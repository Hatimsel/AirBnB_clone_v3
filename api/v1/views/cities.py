#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request
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
        # print(state)
        if state is None:
            abort(404)
        cities = state.cities
        # print(cities)
        if city_id:
            # for city in cities:
            #     if city.id == city_id:
            return (storage.get(City, city_id).to_dict())
        return (city.to_dict() for city in cities)
        # return jsonify(state.to_dict())
    # states = storage.all(State)
    # states = [state.to_dict() for state in states.values()]
    # return jsonify(states)


# @app_views.route("/states/<state_id>",
#                  strict_slashes=False,
#                  methods=['DELETE'])
# def delete_state(state_id):
#     state = storage.get(State, state_id)
#     if state:
#         storage.delete(state)
#         storage.save()
#         return (jsonify({}), 200)
#     abort(404)
#
#
# @app_views.route("/states", strict_slashes=False, methods=['POST'])
# def add_state():
#     if not request.json:
#     # if not request.get_json():
#         return ("Not a JSON\n", 400)
#     if 'name' not in request.get_json():
#         return ("Missing name\n", 400)
#     new_state = State(name=request.get_json()['name'])
#     storage.new(new_state)
#     storage.save()
#     return (new_state.to_dict(), 201)
#
#
# @app_views.route("/states/<state_id>",
#                  strict_slashes=False,
#                  methods=['PUT'])
# def update_state(state_id):
#     if state_id:
#         if not request.json:
#         # if request.get_json() is None:
#             return ("Not a JSON", 400)
#         state = storage.get(State, state_id)
#         if state is None:
#             abort(404)
#         updated_dict = request.get_json()
#         for k, v in updated_dict.items():
#             if k == 'id' or k == 'created_at' or k == 'updated_at':
#                 continue
#             setattr(state, k, v)
#             # state.__dict__[k] = v
#         # storage.new(state)
#         storage.save()
#         return (state.to_dict(), 200)
