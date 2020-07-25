from app import APP
from flask import Flask, render_template
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

    items = [item.details() for item in selection]
    current_items = items[start:end]

    return current_questions

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
    }
    Where actors is a list of all actors in a page
    Or any appropraite error
'''