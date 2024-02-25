#!/usr/bin/python3
"""
Places view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_place(city_id=None, place_id=None):
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = city.places
        places = [place.to_dict() for place in places]
        return (jsonify(places), 200)
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return (jsonify(place.to_dict()), 200)
        abort(404)
    abort(404)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id=None):
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['POST'])
def add_place(city_id=None):
    if city_id is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'user_id' not in request.get_json():
        return ("Missing user_id\n", 400)

    if 'name' not in request.get_json():
        return ("Missing name\n", 400)

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)

    new_place = Place(name=request.get_json()['name'],
                      user_id=request.get_json()['user_id'])

    city.places.append(new_place)

    storage.new(new_place)
    storage.save()

    return (new_place.to_dict(), 201)


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    if place_id:
        if not request.get_json():
            abort(400)

        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        updated_dict = request.get_json()
        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at'\
                    or k == 'user_id' or k == 'city_id':
                continue
            setattr(place, k, v)
        storage.save()
        return (place.to_dict(), 200)
    abort(404)
