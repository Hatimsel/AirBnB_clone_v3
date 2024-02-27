#!/usr/bin/python3
"""
Amenities view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_amenity(amenity_id=None):
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return (jsonify(amenity.to_dict()), 200)
    amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return (jsonify(amenities), 200)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            storage.delete(amenity)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route("/amenities",
                 strict_slashes=False,
                 methods=['POST'])
def add_amenity():
    if request.headers['Content-Type'] != 'application/json':
        abort(400)
    if not request.json:
        abort(400)

    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**request.get_json())

    new_amenity.save()
    # storage.new(new_amenity)
    # storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    if request.headers['Content-Type'] != 'application/json':
        abort(400)
    if amenity_id:
        if not request.get_json():
            abort(400)

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        updated_dict = request.get_json()
        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            setattr(amenity, k, v)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)
    abort(404)
