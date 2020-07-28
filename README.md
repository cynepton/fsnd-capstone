# Udacity Full-Stack Developer Nanodegree Capstone Project
    This project is the final project for my Udacity FullStack Developer Nanodegree.

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This Application does not have a frontend implemented. It is a server only application at the moment.

## Application Heroku Link

**https://fsnd-capstone-cynepton.herokuapp.com/**

## Application Stack

The Application Tech Stack includes:
- **Python3**: The [server language](https://www.python.org/downloads/)
- **Flask**: [Server Framework](https://flask.palletsprojects.com/en/1.1.x/)
- **PostgreSQL**: [Database](https://www.postgresql.org/) of choice
- **SQLAlchemy**: [ORM of choice](https://www.sqlalchemy.org/) to communicate between the python server and the Postgres Database. [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is directly used.
- **Heroku**: [Deployment Platform](https://www.heroku.com/)
- **[Postman](https://www.postman.com/)**: Testing the Application Endpoints

### Application Dependencies

Library     |       Version
----------|---------------
alembic|1.4.2
click|7.1.2
ecdsa|0.15
Flask|1.1.2
Flask-Cors|3.0.8
Flask-Migrate|2.5.3
Flask-Moment|0.10.0
Flask-Script|2.0.6
Flask-SQLAlchemy|2.4.4
future|0.18.2
gunicorn|20.0.4
itsdangerous|1.1.0
Jinja2|2.11.2
jose|1.0.0
Mako|1.1.3
MarkupSafe|1.1.1
psycopg2-binary|2.8.5
pyasn1|0.4.8
pycryptodome|3.3.1
python-dateutil|2.8.1
python-editor|1.0.4
python-jose|3.1.0
python-jose-cryptodome|1.3.2
rsa|4.6
six|1.15.0
SQLAlchemy|1.3.18
Werkzeug|1.0.1


## Working with the application locally
Make sure you have [Python](https://www.python.org/downloads/) installed.

1. **Clone the Repository**
    ```bash
    git clone -b master https://github.com/cynepton/fsnd-capstone.git
    ```

2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/Scripts/activate # for windows
    source env/bin/activate # for MacOs
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Export Environment Variables**
    Refer to the `setup.bash` file and export the environment variables for the project.

5. **Create Local Database**:
    Create a local database and export the database URI as an environment variable with the key `DATABASE_PATH`.

6. **Run Database Migrations**:
    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=myapp
    export FLASK_ENV=development
    flask run
    ```

## Endpoints
The Host for the endpoints is:
`https://fsnd-capstone-cynepton.herokuapp.com/`

OR
`https://localhost:5000/` if the flask app is being run locally.

### Index `/`

The index endpoint that indicates the Flask Application is running normally.<br>
**Response**:<br>
- Type: String
- Body:
    `Udacity FSND Casting Agency App`

### Auth `/auth`

Returns the authorize URL that redirects to the Auth0 login page.<br>
**Response**:<br>
- Type: JSON
- Body:
    ```json
    {
        "url":"https://udacity-fsnd-capstone.us.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=eDxU1gLQJog9fqRGBY7kR3dO7L23QZYB&redirect_uri=https://fsnd-capstone-cynepton.herokuapp.com/"
    }
    ```

### GET `/actors`

Returns a paginated list of actors with a maximum of 10 actors per page<br>
It is a public endpoint available to all three roles<br>
It can take a a `page` argument, the default value is `1`<br>
The page argument indicates the page number to display<br>

When successful,<br>
It returns a status code of `200`, and
```json
{
    "success": true,
    "actors": actors,
    "total": total_actors
}
```
Where `total_actors` is an integer that is the total number of actors in the database<br>
and `actors` is an array of the actors and their details, an example:
```json
[
    {
        "age":23,
        "firstname":"Maisie",
        "gender":"Female",
        "id":1,
        "lastname":"Williams"
    },{
        "age":24,
        "firstname":"Sophie",
        "gender":"Female",
        "id":2,
        "lastname":"Turner"
    },{
        "age":37,
        "firstname":"Henry",
        "gender":"Male",
        "id":3,
        "lastname":"Cavill"
    }
]
```

### POST `/actors`

It takes new actor details as a JSON body<br>
Only the Casting Director and Executive Producer can perform this action<br>
Actor details must have these at minimum:
```json
{
    "firstname": "Keanu",
    "lastname": "Reeves",
    "age": 55,
    "gender": "Male"
}
```
Age must be an integer<br>
There must be no empty or missing entries<br>
It returns a status code of 200, and:<br>
```json
{
    "success": True,
    "actor": actor
}
```
Where actor is a python dictionary (javascript object) of the just added actor details, example:<br>
```json
{
    "id": 20,
    "firstname": "Keanu",
    "lastname": "Reeves",
    "age": 55,
    "gender": "Male"
}
```

### PATCH `/actors/<int:id>`

It takes the actor id to be patched, for example:<br>
`https://fsnd-capstone-cynepton.herokuapp.com/actors/4`
would delete the actor with an id of 4<br>
Only the Casting Director and Executive Producer can perform this action<br>
Actor with the inputted id must exist in the database<br>
It takes the actor details to be updated as a JSON body<br>
Actor details can have all or none of these:<br>
```json
{
    "firstname": "Keanu",
    "lastname": "Reeves",
    "age": 55,
    "gender": "Male"
}
```
Age must be an integer<br>
No key should have a null value<br>
It returns a status code of 200, and:<br>
```json
{
    "success": True,
    "actor": actor
}
```
Where actor is a python dictionary of the actor details<br>

### DELETE `/actors/<int:id>`

where `id` is the existing model id<br>
it responds with a 404 error if `id` is not found<br>
it deletes the corresponding row for `id`<br>
Only the Casting Director and Executive Producer can perform this action<br>
returns a status code of 200 and:
```json
{
    "success": True,
    "delete": id
}
```
where `id` is the id of the deleted record

### GET `/movies`

Returns a paginated list of movies with a maximum of 10 movies per page<br>
It is a public endpoint available to all three roles<br>
It can take a a `page` argument, the default value is `1`<br>
The page argument indicates the page number to display<br>

When successful,<br>
It returns a status code of `200`, and
```json
{
    "success": true,
    "movies": movies,
    "total": total_movies
}
```
Where `total_movies` is an integer that is the total number of movies in the database<br>
and `movies` is an array of the actors and their details, an example:
```json
[
    {
        "description":"A movie about strange things",
        "id":1,
        "release_date":"2020-11-23",
        "title":"Game of Thrones"
    },{
        "description":null,
        "id":2,
        "release_date":"2021-03-13",
        "title":"Justice League: Snyder Cut"
    },{
        "description":null,
        "id":3,
        "release_date":"2021-11-12",
        "title":"The Batman"
    }
]
```

### POST `/movies`

It takes new movie details as a JSON body<br>
Movie details format:
```json
{
    "title": "Avengers: Endgame",
    "release_date": "2019-05-20",
    "description": "movie description",
}
```
The title key must not be null<br>
It returns a status code of 200, and:
```json
{
    "success": True,
    "movie": movie
}
```
Where movie is a python dictionary of the movie details

### PATCH `/actors/<int:id>`

It takes the movie id to be patched, for example:<br>
`https://fsnd-capstone-cynepton.herokuapp.com/movies/4`

Movie with the inputted id must exist in the database<br>
It takes the movie details to be updated as a JSON body<br>
Movie details can have all or none of these:
```json
{
    "title": "Avengers: Endgame",
    "release_date": "2019-05-20",
    "description": "movie description",
}
```
No key should have a null value<br>
Instead omit it completely<br>
If successful:<br>
It returns a status code of 200, and:
```json
{
    "success": True,
    "movie": movie
}
```
Where `movie` is a python dictionary of the movie details

### DELETE `/movies/<int:id>`

where `id` is the existing model id
it responds with a 404 error if `id` is not found
it deletes the corresponding row for `id`
returns status code 200 and:
```json
{
    "success": True,
    "delete": id
}
```
where `id` is the id of the deleted record

## Testing

A postman collection has been created for testing the endpoints.
Import [the file](Udacity-fsnd-capstone.postman_collection.json) into Postman to run the tests.
Adjust the values of the variables `HOST` and the Tokens where appropraite

## Roles and Permissions
The application has 3 roles setup:

1. **Casting Assistant**
    - Can *get* all actors in the database
    - Can *get* all movies in the database

2. **Casting Director**
    - *All permissions* of the casting assistant
    - Can *post* a new actor
    - Can *modify* the details of an existing actor
    - Can *delete* an actor from the database
    - Can *modify* the details of an existing movie

3. **Executive Producer**
    - *All permissions* of the casting director
    - Can *post* a new movie
    - Can *delete* a movie from the database

## Project Structure

```sh
fsnd-capstone
|   .gitattributes
|   .gitignore
|   app.py              # Main flask application file
|   LICENSE
|   manage.py           # Responsible for database migrations on Heroku
|   models.py           # Contains Database Models
|   movies_routes.py    # contains all /movies/* endpoints
|   Procfile            # Heroku Build file
|   README.md
|   requirements.txt    # Contains all application requirements
|   routes.py           # Main routes file also contains all /actors/* endpoints
|   setup.sh
|   test_app.py
|   Udacity-fsnd-capstone.postman_collection.json   # Application tests to be imported into postman
|       
+---auth
|   |   auth.py         # Main Authentication file
|   |   __init__.py
|   |   
|   \---__pycache__
|           auth.cpython-37.pyc
|           __init__.cpython-37.pyc
|           
+---migrations          # Database Migrations Folder
    |   alembic.ini
    |   env.py
    |   README
    |   script.py.mako
    |   
    +---versions
    |   |   430c62f78e2f_.py
    |   |   78e217ad6c1a_.py
    |   |   
    |   \---__pycache__
    |           430c62f78e2f_.cpython-37.pyc
    |           78e217ad6c1a_.cpython-37.pyc
    |           
    \---__pycache__
           env.cpython-37.pyc
```