#!/usr/bin/python3
"""This module defines the routes for handling places in the API"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import user_id


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object based on its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object based on its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        abort(400, "Missing name")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    place = place.to_json()
    return jsonify(place), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """Updates a place object based on its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
