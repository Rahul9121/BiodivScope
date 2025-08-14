#!/usr/bin/env python3
"""
Absolute minimal Flask app for Railway
No imports beyond Flask and basic libraries
"""
import os
import sys

try:
    from flask import Flask, jsonify
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

print(f"✅ Starting Flask app creation...")
print(f"✅ PORT: {os.environ.get('PORT', 'NOT_SET')}")
print(f"✅ Python version: {sys.version}")

# Create app
app = Flask(__name__)

print("✅ Flask app created successfully")

@app.route("/")
def root():
    print("✅ Root endpoint accessed")
    return {"status": "working", "message": "Minimal Flask app is running", "port": os.environ.get('PORT', 'unknown')}

@app.route("/health")
def health():
    print("✅ Health endpoint accessed") 
    return {"status": "healthy", "app": "minimal", "port": os.environ.get('PORT', 'unknown')}

@app.route("/test")
def test():
    print("✅ Test endpoint accessed")
    return {"message": "Test successful!", "version": "minimal-v1"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"✅ Starting Flask development server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    print("✅ Flask app ready for Gunicorn")
