#!/usr/bin/python3
"""This module create a new view for place objects,
handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/citys/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_citys(city_id):
    """Retrieves the list of all place object of a city
    by id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves the list of place object of a given id."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object from Storage by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/citys/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a place object"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    json_data = request.get_json()

    if not json_data:
        abort(400, description="Not a JSON")

    if 'user_id' not in json_data:
        abort(400, description="Missing user_id")

    if 'name' not in json_data:
        abort(400, description="Missing name")

    user_id = json_data['user_id']
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    new_place = Place(**json_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=True)
def update_place(place_id):
    """Update a place object in storage by id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    json_data = request.get_json()

    if json_data is None:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'city_id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
