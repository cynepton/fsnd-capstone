from app import app
from flask import Flask, render_template, abort, jsonify
from flask import request, Response, flash, redirect, url_for
from models import Actors, Movies
import os

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
    })

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