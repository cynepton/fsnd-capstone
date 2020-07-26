from routes import paginate_items, page_limit
from models import Actors, Movies
from app import app
from flask import Flask, render_template, abort, jsonify
from flask import request, Response, flash, redirect, url_for

'''
GET /movies
    It is a public endpoint available to all three roles
    It can take a a page argument,
    that indicates the page number to display
    It returns a status code of 200, and
    {
        "success": True,
        "movies": movies
        "total": total_movies
    }
    Where movies is a list of all movies in a page,
        For Empty description and release_date values,
            null is returned
        total_movies is the total number of movies in the database
    Or any appropraite error
'''


@app.route('/movies')
def get_paginated_movies():

    # Check if the page argument is an integer
    if request.args.get('page'):
        try:
            int(request.args.get('page'))
        except Exception:
            abort(422)

    selection = Movies.query.order_by(Movies.id).all()
    total_movies = len(selection)
    movies = paginate_items(request, selection)

    if len(movies) == 0:
        abort(404)

    return jsonify({
        "success": True,
        "movies": movies,
        "total": total_movies
    }), 200


