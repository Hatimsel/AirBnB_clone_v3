#!/usr/bin/python3
"""
Index with one route
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status",
                 strict_slashes=False,
                 methods=['GET'])
def status():
    """
    Returns the status of our sevrer
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats",
                 strict_slashes=False,
                 methods=['GET'])
def num_of_obj():
    """
    Returns the number of objects
    """
    dict = {}
    classes = {'states': State, 'amenities': Amenity,
               'cities': City, 'places': Place,
               'reviews': Review, 'users': User}
    for name, clas in classes.items():
        dict[name] = storage.count(clas)
    return jsonify(dict)
