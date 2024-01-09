#!/usr/bin/python3
"""This module create a new view for User objects,
handles all default RESTFul API actions.
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all users"""
    all_users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a user object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object from storage by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 204


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User"""
    json_data = request.get_json()
    if json_data is None:
        error_response = jsonify({"error": "Not a JSON"})
        return make_response(error_response, 400)
    if 'name' not in json_data:
        error_response = jsonify({"error": "Missing 'name' in request"})
        return make_response(error_response, 400)
    user_obj = User(**json_data)
    storage.new(user_obj)
    storage.save()
    # user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a Users object in storage by id."""
    json_data = request.get_json()
    if json_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    for k, v in json_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user_obj, k, v)
    storage.save()
    return jsonify(user_obj.to_dict()), 200
