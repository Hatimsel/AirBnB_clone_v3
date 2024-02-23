#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, abort, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_state(state_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    states = storage.all(State)
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def add_state():
    if not request.get_json():
        return ("Not a JSON", 400)
    if 'name' not in request.get_json():
        return ("Missing name", 400)
    new_state = State(name=request.get_json()['name'])
    storage.new(new_state)
    storage.save()
    return (new_state.to_dict(), 201)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    if state_id:
        if not request.get_json():
            return ("Not a JSON", 400)
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        updated_dict = request.get_json()
        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            setattr(state, k, v)
            # state.__dict__[k] = v
        # storage.new(state)
        storage.save()
        return (state.to_dict(), 200)
