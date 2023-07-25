#!/usr/bin/python3
"""create a new view for Review objects that handles all default RestFul API
actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('api/v1/views/places_reviews.py', methods=['GET'], strict_slashes=False)
def get_reviews():
    """Retrieves the list of all Review objects"""
    reviews = []
    for review in storage.all(Review).values():
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    js_info = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.is_json is False:
        abort(400, 'Not a JSON')
    if 'user_id' not in js_info:
        abort(400, 'Missing uer_id')
    if 'text' not in js_info:
        abort(400, 'Missing text')
    review = Review(**js_info)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_reviews(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
