#!/usr/bin/python3
'''Contains the users API.'''
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from models import storage
from models.user import User

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def clean_user_dict(user_dict):
    '''Remove sensitive or unnecessary fields from user dictionary.'''
    user_dict.pop('places', None)
    user_dict.pop('reviews', None)
    return user_dict


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    '''Gets the user or list of users.'''
    if user_id:
        user = storage.get(User, user_id)
        if user:
            return jsonify(clean_user_dict(user.to_dict()))
        raise NotFound()
    all_users = storage.all(User).values()
    users = [clean_user_dict(user.to_dict()) for user in all_users]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    '''Deletes user with the given id.'''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_user():
    '''Adds a new user.'''
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise BadRequest(description='Not a JSON')
    except BadRequest as e:
        raise e
    except Exception:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    user = User(**data)
    user.save()
    return jsonify(clean_user_dict(user.to_dict())), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates the user with the given id.'''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    user = storage.get(User, user_id)
    if user:
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                raise BadRequest(description='Not a JSON')
        except BadRequest as e:
            raise e
        except Exception:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(user, key, value)
        user.save()
        return jsonify(clean_user_dict(user.to_dict())), 200
    raise NotFound()
