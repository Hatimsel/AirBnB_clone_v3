#!/usr/bin/python3
"""
Status of my API
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(error):
    """
    Closes the session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handles error 404
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def not_json(error):
    """
    Handles error 400
    """
    return make_response("Not a JSON\n", 400)


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
