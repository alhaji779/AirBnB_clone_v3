#!/usr/bin/python3
"""
index page for airbnb
"""
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_stat():
    """ returns status """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def get_count():
    """ returns count of data """
    all_dict = {"amenities": 'Amenity',
                "cities": 'City',
                "places": 'Place',
                "reviews": 'Review',
                "states": 'State',
                "users": 'User'}

    for key in count_dict.keys():
        all_dict[key] = storage.count(all_dict.get(key))
    return jsonify(all_dict)
