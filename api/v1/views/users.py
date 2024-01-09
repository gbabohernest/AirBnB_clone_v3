#!/usr/bin/python3
"""This module create a new view for User objects,
handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all user"""
    all_users = []
    for user in storage.all(User).values():
        user_dict = user.to_dict()
        all_users.append(user_dict)
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """Retrieves a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a users"""
    request_data = request.get_json()
    if not request_data:
        error_response = jsonify({"error": "Not a JSON"})
        return make_response(error_response, 400)
    if 'email' not in request_data:
        error_response = jsonify({"error": "Missing email"})
        return make_response(error_response, 400)
    if 'password' not in request_data:
        error_response = jsonify({"error": "Missing password"})
        return make_response(error_response, 400)

    user_obj = User(**request_data)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def post_user(user_id):
    """Updates a user object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    for k, v in request_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(user_obj, k, v)
    storage.save()
    return jsonify(user_obj.to_dict())
