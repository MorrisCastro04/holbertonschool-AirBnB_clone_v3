#!/usr/bin/python3
"""
This module defines the routes for handling states in the API.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all amenities objects.
    """
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_state(amenity_id):
    """
    Retrieves a State object based on its id.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(amenity_id):
    """
    Deletes a State object based on its id.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_state():
    """
    Creates a new State object.
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(amenity_id):
    """
    Updates a State object based on its id.
    """
    amenity_name = storage.get(Amenity, amenity_id)
    if amenity_name is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_name, key, value)
    amenity_name.save()
    return jsonify(amenity_name.to_dict()), 200
