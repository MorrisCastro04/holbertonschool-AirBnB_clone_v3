#!/usr/bin/python3
""" """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

# Creating the Flask app
app = Flask(__name__)

# Registering the blueprint
app.register_blueprint(app_views)


if __name__ == "__main__":

    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')

    app.run(host=host, port=port, threaded=True)


# Status route
@app.teardown_appcontext
def close_storage(self):
    storage.close()


# Error handling
@app.errorhandler(404)
def handle_not_found_error(error):
    """Handles 404 errors by returning a JSON-formatted response"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response
