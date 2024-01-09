#!/usr/bin/python3
"""amenities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all amenities"""
    all_amenities = []
    for amenities in storage.all(Amenity).values():
        amenities_dict = amenities.to_dict()
        all_amenities.append(amenities_dict)
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenities_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_id(amenities_id):
    """Retrieves a amenities object"""
    amenities = storage.get(Amenity, amenities_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<string:amenities_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenities(amenities_id):
    """Deletes a amenities object"""
    amenities = storage.get(Amenity, amenities_id)
    if amenities is None:
        abort(404)
    amenities.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_amenities():
    """Creates a amenities"""
    request_data = request.get_json()
    if request_data is None:
        error_response = jsonify({"error": "Not a JSON"})
        return make_response(error_response, 400)
    if 'name' not in request_data:
        error_response = jsonify({"error": "Missing name"})
        return make_response(error_response, 400)
    amenities_obj = Amenity(**request_data)
    amenities_obj.save()
    return jsonify(amenities_obj.to_dict()), 201


@app_views.route('/amenities/<string:amenities_id>', methods=['PUT'],
                 strict_slashes=False)
def post_amenities(amenities_id):
    """Updates a amenities object"""
    request_data = request.get_json()
    if request_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenities_obj = storage.get(Amenity, amenities_id)
    if amenities_obj is None:
        abort(404)
    for k, v in request_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenities_obj, k, v)
    storage.save()
    return jsonify(amenities_obj.to_dict())
