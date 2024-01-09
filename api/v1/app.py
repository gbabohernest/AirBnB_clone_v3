#!/usr/bin/python3
"""This module creates an instance of flask and register
   blueprints app_views to flask instance app
"""
from flask import Flask
from flask.json import jsonify
from models import storage
from api.v1.views import app_views
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(obj):
    """ calls storage.close() """
    storage.close()


@app.errorhandler(404)
def bad_request_404(e):
    """Handler for 404 errors.
    return: JSON-formatted 404 status code
    """
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    from os import getenv

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))

    app.run(host=host, port=port, threaded=True)
