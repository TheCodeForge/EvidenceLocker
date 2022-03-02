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

    g.db=db_session()

@app.after_request
def after_request(resp):
    
    resp.headers["Content-Security-Policy"] = "default-src 'self'; script-src code.jquery.com cdn.jsdelivr.net; object-src 'none'; style-src 'self'; img-src 'self'; media-src: 'none'; frame-src 'none'; font-src 'none'; connect-src 'self'; form-action 'self'; plugin-types 'none';"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(self)"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"
    
    return resp
