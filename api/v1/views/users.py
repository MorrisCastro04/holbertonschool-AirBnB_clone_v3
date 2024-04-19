#!/usr/bin/python3
"""This module defines the routes for handling users in the API"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users(user_id):
    """Retrieves the list of all user objects"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object based on its id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object based on its id"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}, 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """Creates a new user object"""
    
    if not request.is_json:
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """Updates a user object based on its id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
