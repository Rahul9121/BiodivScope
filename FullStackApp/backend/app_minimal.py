#!/usr/bin/env python3
"""
Absolute minimal Flask app for Railway
No imports beyond Flask and basic libraries
"""
try:
    from flask import Flask, jsonify
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import failed: {e}")
    exit(1)

# Create app
app = Flask(__name__)

@app.route("/")
def root():
    return {"status": "working", "message": "Minimal Flask app is running"}

@app.route("/health")
def health():
    return {"status": "healthy", "app": "minimal"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting on port {port}")
    app.run(host="0.0.0.0", port=port)
