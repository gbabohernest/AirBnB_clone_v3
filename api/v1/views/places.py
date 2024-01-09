#!/usr/bin/python3
"""This module create a new view for place objects,
handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage

from models.place import Place
from models.city import City

@app_views.route('/citys/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_citys(city_id):
    """Retrieves the list of all place object of a city
    by id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves the list of place object of a given id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/place_id', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object from Storage by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/citys/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a place object"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    new_place = Place()
    new_Place.city_id = city_id
    new_place.name = data.get('name')
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=True)
def update_place(place_id):
    """Update a place object in storage by id"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200