#!/usr/bin/python3
"""Creates route /status on object app_views.
   return: JSON
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import Flask


@app_views.route('/status', strict_slashes=False)
def status():
    """
     returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """retrieves the number of each objects by type:"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
