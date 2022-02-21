from os import environ
import secrets

from flask import *
from flaskext.markdown import Markdown

from sqlalchemy import *

app=Flask(__name__)

app.url_map.strict_slashes=False

app.before_request
def before_request():

    session.permanent=True

@app.get('/')
def home():
    return "placeholder page"