from app import app
from flask import Flask, render_template, abort, jsonify
from flask import request, Response, flash, redirect, url_for
from models import Actors, Movies
import os
import json
from sqlalchemy import exc

from auth.auth import AuthError, requires_auth

# Max items per page
page_limit = os.environ['ITEMS_PER_PAGE']

'''
paginate_items()
    This function takes in a query list of items
    and returns a particular list of items per page
'''


def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * page_limit
    end = start + page_limit

    if start is '':
        start = 0

    items = [item.details() for item in selection]
    current_items = items[int(start):int(end)]

    return current_items


# ACTORS
# --------------------------------------------------------- #


'''
GET /actors
    It is a public endpoint available to all three roles
    It can take a a page argument,
    that indicates the page number to display
    It returns a status code of 200, and
    {
        "success": True,
        "actors": actors
        "total": total_actors
    }
    Where actors is a list of all actors in a page,
        total_actors is the total number of actors in the database
    Or any appropraite error
'''


@app.route('/')
def index_endpoint():
    return "Udacity FSND Casting Agency App"


@app.route('/actors')
def get_paginated_actors():

    # Check if the page argument is an integer
    if request.args.get('page'):
        try:
            int(request.args.get('page'))
        except Exception:
            abort(422)

    selection = Actors.query.order_by(Actors.id).all()
    total_actors = len(selection)
    actors = paginate_items(request, selection)

    if len(actors) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "actors": actors,
        "total": total_actors
    }), 200


'''
POST /actors
    It takes new actor details as a JSON body
    Actor details must have these at minimum:
    {
        "firstname": "Keanu",
        "lastname": "Reeves",
        "age": 55,
        "gender": "Male"
    }
    Age must be a number
    There must be no empty or missing entries
    It returns a status code of 200, and:
    {
        "success": True,
        "actor": actor
    }
    Where actor is a python dictionary of the actor details
'''


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(jwt):
    # Gets the JSON body
    data = request.get_json()
    # print(data)

    # Checks that the JSON contains the complete details
    if 'firstname' not in data:
        abort(422)
    if 'lastname' not in data:
        abort(422)
    if 'gender' not in data:
        abort(422)
    if 'age' not in data:
        abort(422)

    # Checks that the age is an integer
    try:
        int(data.get('age'))
    except Exception:
        abort(400)

    # Gets each actor detail
    actor_firstname = data.get('firstname')
    actor_lastname = data.get('lastname')
    actor_age = int(data.get('age'))
    actor_gender = data.get('gender')

    # Checks that the details are not empty
    if actor_firstname is None:
        abort(400)
    if actor_lastname is None:
        abort(400)
    if actor_age is None:
        abort(400)
    if actor_gender is None:
        abort(400)

    # Initiates an instance of the Actors row
    new_actor = Actors(
        firstname=actor_firstname,
        lastname=actor_lastname,
        age=actor_age,
        gender=actor_gender
    )

    try:
        # Insert the new actor details into the database
        new_actor.insert()
    except Exception:
        abort(422)

    actor = new_actor.details()

    return jsonify({
        "success": True,
        "actor": actor
    }), 200


'''
PATCH /actors/<int:id>
    It takes the actor id
    Actor with the inputted id must exist in the database
    It takes the actor details to be updated as a JSON body
    Actor details can have all or none of these:
    {
        "firstname": "Keanu",
        "lastname": "Reeves",
        "age": 55,
        "gender": "Male"
    }
    Age must be an integer
    Each key must not have a null value
    It returns a status code of 200, and:
    {
        "success": True,
        "actor": actor
    }
    Where actor is a python dictionary of the actor details
'''


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(jwt, id):

    # Get the id of the actor to be updated
    actor_to_patch = Actors.query.get(id)
    # Return a 404 error if the id doesn't exist
    if actor_to_patch is None:
        abort(404)

    # Get the JSON body
    data = request.get_json()

    # Update the actor details
    # Return a 400 error if the key values are null
    if 'firstname' in data:

        if data.get('firstname') is None:
            abort(400)

        actor_to_patch.firstname = data.get('firstname')

    if 'lastname' in data:

        if data.get('lastname') is None:
            abort(400)

        actor_to_patch.lastname = data.get('lastname')

    if 'age' in data:

        if data.get('age') is None:
            abort(400)

        actor_to_patch.age = data.get('age')

    if 'gender' in data:

        if data.get('gender') is None:
            abort(400)

        actor_to_patch.gender = data.get('gender')

    # Add the new details to the the database
    try:
        actor_to_patch.update()
    except Exception:
        abort(422)

    actor = actor_to_patch.details()

    return jsonify({
        "success": True,
        "actor": actor
    }), 200


'''
DELETE /actors/<int:id>
        where <id> is the existing model id
        it responds with a 404 error if <id> is not found
        it deletes the corresponding row for <id>
    returns status code 200 and json
    {
        "success": True,
        "delete": id
    }
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(jwt, id):
    actor_to_delete = Actors.query.get(id)
    if actor_to_delete is None:
        abort(404)

    id = actor_to_delete.id

    try:
        actor_to_delete.delete()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    }), 200


# ACTORS
# --------------------------------------------------------- #
from movies_routes import *


'''
@app.errorhandlers
    Error handlers for expected errors
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def processAuthError(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code

    return jsonify({
        "success": False,
        "error": status_code,
        "message": message
    }), status_code
