#!/usr/bin/python3
""" index file
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def showStat():
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def getCount():
    all_dict = {"amenities": 'Amenity',
                  "cities": 'City',
                  "places": 'Place',
                  "reviews": 'Review',
                  "states": 'State',
                  "users": 'User'}
    for key in all_dict.keys():
        all_dict[key] = storage.count(all_dict.get(key))
    return jsonify(all_dict)
