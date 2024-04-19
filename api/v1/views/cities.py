#!/usr/bin/python3
"""
This module defines the routes for handling states in the API.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_all_cities(state_id):
    """
    Retrieves all cities of a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a city by its ID
    """
    city_name = storage.get(City, city_id)
    if city_name is None:
        abort(404)
    return jsonify(city_name.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a city by its ID
    """
    city_name = storage.get(City, city_id)
    if city_name is None:
        abort(404)
    storage.delete(city_name)
    storage.save()
    return jsonify({}, 200)


@app_views.route("/states/<states_id>/cities",
                 methods=["POST"], strict_slashes=False)
def post_city(states_id):
    """
    Creates a new city
    """
    state_name = storage.get(State, states_id)
    if not state_name:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()
    city = City(**data)
    city.state_id = states_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    Updates a city by its ID
    """
    city_name = storage.get(City, city_id)
    if city_name is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_name, key, value)
    storage.save()
    return jsonify(city_name.to_dict()), 200
