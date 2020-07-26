from routes import paginate_items, page_limit
from models import Actors, Movies
from app import app
from flask import Flask, render_template, abort, jsonify
from flask import request, Response, flash, redirect, url_for

