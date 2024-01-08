#!/usr/bin/python3
"""Creates route /status on object app_views.
   return: JSON
"""

from api.v1.views import app_views
from flask import jsonify
from flask import Flask


@app_views.route('/status', strict_slashes=False)
def status():
    """
     returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})
