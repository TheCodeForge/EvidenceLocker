from os import environ
import secrets

from flask import *
from flaskext.markdown import Markdown

from sqlalchemy import *
from sqlalchemy.pool import Queuepool

app=Flask(__name__)