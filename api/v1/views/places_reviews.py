#!/usr/bin/python3
"""create a new view for User objects that handles all default RestFul API
actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    """Retrieves the list of all User objects"""
    reviews = []
    for review in storage.all(Review).values():
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<reviews_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(reviews_id):
    """Retrieves a User object"""
    review = storage.get(Review, reviews_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<reviews_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(reviews_id):
    """Deletes a User object"""
    review = storage.get(Review, reviews_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_reviews(place_id):
    """Creates a User"""
    js_info = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    if 'uer_id' not in js_info:
        abort(400, 'Missing uer_id')
    if 'text' not in js_info:
        abort(400, 'Missing text')
    review = Review(**js_info)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
