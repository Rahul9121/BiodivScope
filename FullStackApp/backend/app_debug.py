#!/usr/bin/env python3
"""
Ultra-minimal Railway app for debugging
Includes extensive logging to debug deployment issues
"""
import os
import sys
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log Python and environment info
logger.info(f"Python version: {sys.version}")
logger.info(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
logger.info(f"All environment variables: {list(os.environ.keys())}")

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'debug-secret-key')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')

logger.info(f"Flask app created successfully")
logger.info(f"App config ENV: {app.config['ENV']}")

# Root and health endpoints
@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return jsonify({
        "status": "running",
        "message": "BiodivScope Debug API - Root endpoint",
        "endpoints": ["/", "/health", "/test", "/debug"]
    }), 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Railway"""
    logger.info("Health endpoint accessed")
    return jsonify({
        "status": "healthy",
        "message": "BiodivScope Debug API is healthy",
        "version": "1.0.0",
        "environment": app.config['ENV'],
        "port": os.environ.get('PORT', 'unknown')
    }), 200

@app.route("/test", methods=["GET"])
def test():
    """Basic test endpoint"""
    logger.info("Test endpoint accessed")
    return jsonify({
        "message": "Test successful!",
        "port": os.environ.get('PORT', 'unknown'),
        "environment": app.config['ENV'],
        "python_version": sys.version
    }), 200

@app.route("/debug", methods=["GET"])
def debug():
    """Debug info endpoint"""
    logger.info("Debug endpoint accessed")
    return jsonify({
        "environment_variables": dict(os.environ),
        "flask_config": dict(app.config),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "python_path": sys.path
    }), 200

# Add error handling
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {error}")
    return jsonify({
        "status": "error",
        "message": str(error),
        "type": type(error).__name__
    }), 500

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5001))
        logger.info(f"Starting Flask app on host=0.0.0.0, port={port}")
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start app: {e}")
        sys.exit(1)
