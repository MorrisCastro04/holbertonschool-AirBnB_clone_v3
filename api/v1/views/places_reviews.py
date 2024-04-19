#!/usr/bin/python3
"""This module defines the routes for handling reviews in the API"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object based on its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if "user_id" is None:
        abort(404)
    if "text" not in request.get_json():
        abort(400, "Missing text")
    data = request.get_json()
    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
