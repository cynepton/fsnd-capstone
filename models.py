from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json

db = SQLAlchemy()
migrate = Migrate()


# Path is stored in the virtual environment
# with a key name of DATABASE_PATH
database_path = os.environ['DATABASE_PATH']
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


'''
Movies
    The table containing movies and their details
'''


class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), nullable=False, unique=True)
    release_date = db.Column(db.String())
    description = db.Column(db.String())

    '''
    insert()
        inserts a new model into a database
        the model must have a unique title
        the model must have a unique id or null id
        EXAMPLE
            movie = Movies(title=req_title, release_date=req_release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movies.query.filter(Movies.id == id).one_or_none()
            movie.title = 'Wonder Woman 1984'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movies(title=req_title, release_date=req_release_date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    details()
        details on each movie
    '''
    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'description': self.description
        }


'''
Actors
    The table containing actors and their details
'''


class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(32), nullable=False)

    '''
    insert()
        inserts a new model into a database
        the model must have a unique title
        the model must have a unique id or null id
        EXAMPLE
            actor = Actors(firstname=Keanu, lastname=Reeves)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actors.query.filter(Actors.id == id).one_or_none()
            actor.lastname = 'Cavill'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actors(firstname=Keanu, lastname=Reeves)
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    details()
        details on each actor
    '''
    def details(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender
        }
