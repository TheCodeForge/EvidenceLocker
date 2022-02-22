from os import environ
import secrets

import alembic.config

from flask import *
from flaskext.markdown import Markdown

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session

app=Flask(
    __name__,
    template_folder='./templates',
    static_folder='./assets'
    )


app.url_map.strict_slashes=False

#===CONFIGS===
app.config['DATABASE_URL']                  = environ.get("DATABASE_URL",'').replace("postgres://", "postgresql://")
if not app.config['DATABASE_URL']:
    cfg=alembic.config.Config('alembic.ini')
    app.config['DATABASE_URL']=cfg.get_main_option('sqlalchemy.url')
    del cfg

app.config["PERMANENT_SESSION_LIFETIME"]    = 60 * 60
app.config["SESSION_REFRESH_EACH_REQUEST"]  = True
app.config['SECRET_KEY']                    = environ.get("SECRET_KEY")
app.config['SERVER_NAME']                   = environ.get("SERVER_NAME")


#===EXTENSIONS

Markdown(app)


#===SQLALCHEMY===
_engine=create_engine(
    app.config['DATABASE_URL'],
    pool_use_lifo=True
)
db_session=scoped_session(
    sessionmaker(
        bind=_engine
        )
    )
Base=declarative_base()

from .classes import *
from .routes import *


@app.before_request
def before_request():

    session.permanent=True

