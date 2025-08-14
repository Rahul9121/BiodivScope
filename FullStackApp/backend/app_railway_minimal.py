"""
Ultra-minimal Railway app for debugging
This strips out all complex dependencies and imports
"""
import os
from flask import Flask, jsonify

# Create minimal Flask app
app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')

# Health check endpoint
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "message": "BiodivScope Minimal API is running",
        "version": "1.0.0",
        "environment": app.config['ENV']
    }), 200

@app.route("/test", methods=["GET"])
def test():
    """Basic test endpoint"""
    return jsonify({
        "message": "Test successful!",
        "port": os.environ.get('PORT', 'unknown'),
        "environment": app.config['ENV']
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
