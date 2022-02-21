from os import environ
import secrets

from flask import *
from flaskext.markdown import Markdown

from sqlalchemy import *

app=Flask(
    __name__,
    template_folder='./templates',
    static_folder='./assets'
    )

app.url_map.strict_slashes=False

#map config vars
config_vars=[
    "SECRET_KEY",
    "SERVER_NAME"
]
for x in config_vars:
    app.config[x]=environ.get(x)

@app.before_request
def before_request():

    session.permanent=True

@app.get('/')
def home():
    return "placeholder page"