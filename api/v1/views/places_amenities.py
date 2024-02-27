#!/usr/bin/python3
"""
Places Amenities view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_place_amenity(place_id=None):
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = place.amenities
        if amenities:
            amenities = [amenity.to_dict() for amenity in amenities]
            return (jsonify(amenities), 200)
        return (jsonify([]), 200)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place_amenity(place_id=None, amenity_id=None):
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = place.amenities
        for amenity in amenities:
            if amenity.id == amenity_id:
                storage.delete(amenity)
                storage.save()
                break
                return (jsonify({}), 200)
        abort(404)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['POST'])
def add_place_amenity(place_id=None, amenity_id=None):
    """
    Links a Amenity obj to a Place
    """
    if place_id is None or amenity_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        place.amenities.append(amenity)
        storage.save()
        return (amenity.to_dict(), 201)
    else:
        return (amenity.to_dict(), 200)
