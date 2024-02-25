#!/usr/bin/python3
"""
Reviews view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_review(place_id=None, review_id=None):
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        reviews = place.reviews
        reviews = [review.to_dict() for review in reviews]
        return (jsonify(reviews), 200)
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            return (jsonify(review.to_dict()), 200)
        abort(404)
    abort(404)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            storage.delete(review)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['POST'])
def add_review(place_id=None):
    if place_id is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)

    if 'text' not in request.get_json():
        return ("Missing text\n", 400)

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)

    new_review = Review(text=request.get_json()['text'],
                        user_id=request.get_json()['user_id'])

    place.reviews.append(new_review)

    storage.new(new_review)
    storage.save()

    return (new_review.to_dict(), 201)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    if review_id:
        if not request.get_json():
            abort(400)

        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        updated_dict = request.get_json()
        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at'\
                    or k == 'user_id' or k == 'place_id':
                continue
            setattr(review, k, v)
        storage.save()
        return (review.to_dict(), 200)
    abort(404)
