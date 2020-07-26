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


'''
POST /movies
    It takes new movie details as a JSON body
    Movie details format:
    {
        "title": "Avengers: Endgame",
        "release_date": "2019-05-20",
        "description": "movie description",
    }
    The title key must not be null
    It returns a status code of 200, and:
    {
        "success": True,
        "movie": movie
    }
    Where movie is a python dictionary of the movie details
'''


@app.route('/movies', methods=['POST'])
def post_movie():
    # Gets the JSON body
    data = request.get_json()
    # print(data)

    # Checks that the JSON contains the complete details
    if 'title' not in data:
        abort(422)

    # Gets each movie detail
    movie_title = data.get('title')
    movie_release_date = None
    movie_description = None

    if 'release_date' in data:
        movie_release_date = data.get('release_date')

    if 'description' in data:
        movie_description = data.get('description')

    # Checks that the movie title is not empty
    if movie_title is None:
        abort(400)

    # Initiates an instance of the Movies row
    new_movie = Movies(
        title=movie_title,
        release_date=movie_release_date,
        description=movie_description
    )
    try:
        # Insert the new movie details into the database
        new_movie.insert()
    except Exception:
        abort(422)

    movie = new_movie.details()

    return jsonify({
        "success": True,
        "movie": movie
    }), 200


