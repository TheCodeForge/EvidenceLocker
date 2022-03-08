from gevent import monkey
monkey.patch_all()

from os import environ
import secrets
import time

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

app.config["HCAPTCHA_SECRET"]               = environ.get("HCAPTCHA_SECRET")
app.config["HCAPTCHA_SITEKEY"]              = environ.get("HCAPTCHA_SITEKEY")
app.config["PERMANENT_SESSION_LIFETIME"]    = 60 * 60
app.config["SESSION_REFRESH_EACH_REQUEST"]  = True
app.config['SECRET_KEY']                    = environ.get("SECRET_KEY")
app.config['SERVER_NAME']                   = environ.get("SERVER_NAME")

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

#===CLASSES AND ROUTES

from .routes import *

#===EXTENSIONS

Markdown(app)

#===BEFORE/AFTER REQS===

@app.before_request
def before_request():

    session.permanent=True

    g.db=db_session()
    
    g.time=int(time.time())

@app.after_request
def after_request(resp):
    
    resp.headers["Content-Security-Policy"] = "default-src * data:; script-src hcaptcha.com code.jquery.com cdn.jsdelivr.net ; object-src 'none'; style-src 'self'; media-src 'none';"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(self)"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"
    
    return resp
