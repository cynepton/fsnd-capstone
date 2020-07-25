from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# Path is stored in the virtual environment
# with a key name of DATABASE_PATH 
database_path = os.environ['DATABASE_PATH']
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def db_setup(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
