#!/usr/bin/python3
"""
Cities view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_city(state_id=None, city_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = state.cities
        cities = [city.to_dict() for city in cities]
        return (jsonify(cities), 200)
    if city_id:
        city = storage.get(City, city_id)
        if city:
            return (jsonify(city.to_dict()), 200)
        abort(404)
    abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id=None):
    if city_id:
        city = storage.get(City, city_id)
        if city:
            storage.delete(city)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def add_city(state_id=None):
    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    if state_id is None or storage.get(State, state_id) is None:
        abort(404)

    if not request.json:
        abort(400)

    if 'name' not in request.get_json():
        return ("Missing name\n", 400)

    new_city = City(name=request.get_json()['name'])

    state = storage.get(State, state_id)
    state.cities.append(new_city)

    storage.new(new_city)
    storage.save()

    return (new_city.to_dict(), 201)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    if city_id:
        if not request.get_json():
            abort(400)

        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        updated_dict = request.get_json()
        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            setattr(city, k, v)
        storage.save()
        return (city.to_dict(), 200)
    abort(404)
