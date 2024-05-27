#!/usr/bin/python3
""" index file
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def show_stat():
    """Returns the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def get_count():
    """Returns the count of all objects by type"""
    all_dict = {
        "amenities": 'Amenity',
        "cities": 'City',
        "places": 'Place',
        "reviews": 'Review',
        "states": 'State',
        "users": 'User'
    }
    for key in all_dict.keys():
        all_dict[key] = storage.count(all_dict[key])
    return jsonify(all_dict)
