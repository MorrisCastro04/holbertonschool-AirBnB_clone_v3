#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of each object by type"""
    stats = {}

    # Get the count of each object type
    stats['amenities'] = storage.count('Amenity')
    stats['cities'] = storage.count('City')
    stats['places'] = storage.count('Place')
    stats['reviews'] = storage.count('Review')
    stats['states'] = storage.count('State')
    stats['users'] = storage.count('User')

    return jsonify(stats)
