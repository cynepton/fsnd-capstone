import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from models import db_setup

'''
App Config
    Creates the flask app
'''


def create_app(test_config=None):
    # create and configure the app
    # app = Flask(__name__)
    app = Flask(__name__)
    db = db_setup(app)
    CORS(app)

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

'''
Models
    Imports models from models.py file
'''
from models import db, Actors, Movies

'''
@app.routes()
    Imports endpoints from routes.py file
'''
from routes import *