#!/usr/bin/python3
"""
Users view
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=['GET'])
@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['GET'])
def retrieve_user(user_id=None):
    if user_id:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users)


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route("/users",
                 strict_slashes=False,
                 methods=['POST'])
def add_user():
    if not request.get_json():
        abort(400)

    if 'email' not in request.get_json():
        return ("Missing email\n", 400)
    if 'password' not in request.get_json():
        return ("Missing password\n", 400)

    new_user = User(email=request.get_json()['email'],
                    password=request.get_json()['password'])
    storage.new(new_user)
    storage.save()

    return (new_user.to_dict(), 201)


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):

    if user_id:
        if request.get_json() is None:
            abort(400)
        user = storage.get(User, user_id)

        if user is None:
            abort(404)
        updated_dict = request.get_json()

        for k, v in updated_dict.items():
            if k == 'id' or k == 'created_at'\
                    or k == 'updated_at' or k == 'email':
                continue
            setattr(user, k, v)

        storage.save()
        return (user.to_dict(), 200)
