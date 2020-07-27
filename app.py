import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from models import db_setup
from auth.auth import AUTH0_DOMAIN, API_AUDIENCE

'''
App Config
    Creates the flask app
'''

AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']

def create_app(test_config=None):
    # create and configure the app
    # app = Flask(__name__)
    app = Flask(__name__)
    db = db_setup(app)
    CORS(app)

    return app

app = create_app()
if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=8080, debug=True)
    app.run(port=8080, debug=True)


@app.route("/auth")
def generate_auth_url():
    url = f'https://{AUTH0_DOMAIN}/authorize' \
        f'?audience={API_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{AUTH0_CLIENT_ID}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'
        
    return jsonify({
        'url': url
    })


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