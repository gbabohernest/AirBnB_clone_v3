#!/usr/bin/python3
"""This module create a new view for Place objects,
handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, description="Not a JSON")
    if 'user_id' not in req_json:
        abort(400, description="Missing user_id")
    if 'name' not in req_json:
        abort(400, description="Missing name")

    user_id = req_json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_place = Place(**req_json)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, description="Not a JSON")

    for key, value in req_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for Place objects based on JSON in the request body"""
    try:
        search_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if not search_data or all(len(value) == 0 for value in
                              search_data.values()):
        # Retrieve all Place objects if the JSON body is empty
        # or each list is empty
        places = storage.all(Place).values()
    else:
        # Filter based on the search criteria
        places = set()

        if 'states' in search_data:
            for state_id in search_data['states']:
                state = storage.get(State, state_id)
                if state:
                    places.update(state.places)

        if 'cities' in search_data:
            for city_id in search_data['cities']:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

        if 'amenities' in search_data:
            amenities = set(search_data['amenities'])
            places = [place for place in places if
                      amenities.issubset(place.amenities)]

    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)
