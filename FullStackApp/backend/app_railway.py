import os
import json
import psycopg2
from flask import Flask, request, jsonify, session, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import logging
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_caching import Cache
import pandas as pd
from config import Config

# Import your existing routes and modules
try:
    from backend.routes.account_routes import account_bp
    from backend.routes.location_routes import location_bp
except ImportError:
    # Handle imports for Railway deployment structure
    try:
        from routes.account_routes import account_bp
        from routes.location_routes import location_bp
    except ImportError:
        # Create minimal blueprints if routes don't exist
        from flask import Blueprint
        account_bp = Blueprint('account', __name__)
        location_bp = Blueprint('locations', __name__)
        
        @account_bp.route('/test')
        def account_test():
            return jsonify({"message": "Account routes not available yet"})
            
        @location_bp.route('/test')
        def location_test():
            return jsonify({"message": "Location routes not available yet"})

# Handle heavy ML dependencies gracefully
try:
    from backend.mitigation_action import (
        generate_mitigation_report,
        query_mitigation_action,
        threat_level_from_code
    )
except ImportError:
    try:
        from mitigation_action import (
            generate_mitigation_report,
            query_mitigation_action,
            threat_level_from_code
        )
    except ImportError:
        # Create dummy functions if ML modules aren't available
        def generate_mitigation_report(*args, **kwargs):
            return {"message": "ML features not available yet"}
            
        def query_mitigation_action(*args, **kwargs):
            return {"message": "ML features not available yet"}
            
        def threat_level_from_code(*args, **kwargs):
            return "unknown"

import xlsxwriter
import traceback

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize extensions
cache = Cache(app)

# Configure CORS for production
cors_origins = app.config['CORS_ORIGINS']
if app.config['ENV'] == 'production':
    CORS(app, resources={r"/*": {"origins": cors_origins}}, supports_credentials=True)
else:
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Register blueprints
app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(location_bp, url_prefix="/locations")

# Configure logging
logging.basicConfig(level=logging.INFO if app.config['ENV'] == 'production' else logging.DEBUG)

# Session configuration
Session(app)

# Database configuration
def get_db_config():
    """Get database configuration from environment variables"""
    if app.config.get('DATABASE_URL'):
        # Railway provides DATABASE_URL
        return app.config['DATABASE_URL']
    else:
        # Fallback to individual config variables
        return {
            'host': app.config['DB_HOST'],
            'user': app.config['DB_USER'],
            'password': app.config['DB_PASSWORD'],
            'dbname': app.config['DB_NAME'],
            'port': app.config['DB_PORT']
        }

DB_CONFIG = get_db_config()
GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

# Health check endpoint for Railway
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "message": "BiodivScope Backend API is running",
        "version": "1.0.0",
        "environment": app.config['ENV']
    }), 200

@app.route("/session-risks", methods=["GET"])
def get_session_risks():
    return jsonify({"risks": session.get("risks", [])})

@app.before_request
def log_request():
    if app.config['ENV'] != 'production':
        print(f"🔍 Request: {request.method} {request.path}")
        if request.method in ["POST", "PUT"]:
            print(f"Body: {request.get_data(as_text=True)}")

def connect_db():
    try:
        if isinstance(DB_CONFIG, str):
            # DATABASE_URL format
            return psycopg2.connect(DB_CONFIG)
        else:
            # Dictionary format
            return psycopg2.connect(**DB_CONFIG)
    except Exception as err:
        print(f"DB connection error: {err}")
        return None

# Get Latitude, Longitude from ZIP Code
def get_lat_lon_from_zip(zipcode):
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"postalcode": zipcode, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200 and response.json():
            data = response.json()[0]
            latitude = float(data["lat"])
            longitude = float(data["lon"])
            return latitude, longitude
        else:
            return 40.0583, -74.4057  # Default coordinates for New Jersey

    except Exception as e:
        print(f"Error fetching ZIP code data: {e}")
        return 40.0583, -74.4057  # Default fallback coordinates

def get_lat_lon_from_address(address):
    """
    Fetch latitude, longitude, and ZIP code for a given address using Nominatim API.
    Adjusts query parameters to avoid conflicts.
    """
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": address, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if app.config['ENV'] != 'production':
            print(f"API Request URL: {response.url}")
            print(f"API Response Status: {response.status_code}")

        if response.status_code == 200:
            json_response = response.json()
            
            if json_response:
                data = json_response[0]
                latitude = float(data["lat"])
                longitude = float(data["lon"])

                # Extract ZIP Code if available
                address_parts = data.get("display_name", "").split(",")
                zip_code = address_parts[-2].strip() if len(address_parts) > 1 else None

                return latitude, longitude, zip_code
            else:
                print("No results found for the address.")
                return None, None, None
        else:
            print(f"Nominatim API Error: {response.status_code}")
            return None, None, None

    except Exception as e:
        print(f"Error fetching address data: {e}")
        return None, None, None

@app.route("/address-autocomplete", methods=["GET"])
def address_autocomplete():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": query, "countrycodes": "us", "format": "json", "limit": 5},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200:
            suggestions = [
                {"display_name": item.get("display_name", "")}
                for item in response.json()
                if "New Jersey" in item.get("display_name", "")
            ]
            return jsonify(suggestions)
        else:
            print(f"Nominatim API returned status {response.status_code}")
            return jsonify([])
    except Exception as e:
        print(f"Error fetching autocomplete data: {e}")
        return jsonify([])

def standardize_threat_status(status):
    mapping = {
        "critically endangered": "high",
        "endangered": "high",
        "vulnerable": "moderate",
        "near threatened": "moderate",
        "least concern": "low",
        "data deficient": "unknown",
        "extinct": "high",
        "extinct in the wild": "high",
        "unknown": "low"
    }
    return mapping.get(status.lower(), "low")

# Basic API endpoints for testing
@app.route('/api/test', methods=['GET'])
def api_test():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "BiodivScope API is working!",
        "status": "success",
        "endpoints": {
            "health": "/health",
            "address_autocomplete": "/address-autocomplete",
            "session_risks": "/session-risks",
            "account_test": "/account/test",
            "location_test": "/locations/test"
        }
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    try:
        # Test database connection
        db_status = "connected" if connect_db() else "disconnected"
    except:
        db_status = "error"
    
    return jsonify({
        "api": "running",
        "database": db_status,
        "environment": app.config['ENV'],
        "version": "1.0.0"
    })

# Copy your existing routes here...
# [The rest of your app.py routes would go here]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])
