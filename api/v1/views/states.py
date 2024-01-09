#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State"""
    all_states = []
    for state in storage.all(State).values():
        state_dict = state.to_dict()
        all_states.append(state_dict)
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a State"""
    request_data = request.get_json()
    if request_data is None:
        error_response = jsonify({"error": "Not a JSON"})
        return make_response(error_response, 400)
    if 'name' not in request_data:
        error_response = jsonify({"error": "Missing name"})
        return make_response(error_response, 400)
    state_obj = State(**request_data)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def post_state(state_id):
    """Updates a State object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    for k, v in request_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, k, v)
    storage.save()
    return jsonify(state_obj.to_dict())