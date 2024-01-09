#!/usr/bin/python3
"""This module create a new view for User objects,
handles all default RESTFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', method=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', method=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """Retrieves the list of User objects"""

    if user_id is None:
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])

    else:
        # id is present
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', method=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object from storage by id"""

    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', method=['CREATE'], strict_slashes=False)
def create_users():
    """Creates a User object"""

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', method=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object in storage by id."""

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
