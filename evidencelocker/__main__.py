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

from werkzeug.middleware.proxy_fix import ProxyFix

app=Flask(
    __name__,
    template_folder='./templates',
    static_folder='./assets'
    )

app.url_map.strict_slashes=False

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)

#===CONFIGS===
app.config['DATABASE_URL']                  = environ.get("DATABASE_URL",'').replace("postgres://", "postgresql://")
if not app.config['DATABASE_URL']:
    cfg=alembic.config.Config('alembic.ini')
    app.config['DATABASE_URL']=cfg.get_main_option('sqlalchemy.url')
    del cfg

app.config["HCAPTCHA_SECRET"]               = environ.get("HCAPTCHA_SECRET")
app.config["HCAPTCHA_SITEKEY"]              = environ.get("HCAPTCHA_SITEKEY")
app.config["MAILGUN_KEY"]                   = environ.get("MAILGUN_KEY")
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
from .helpers.filters import *
from .helpers.hashes import generate_hash

#===EXTENSIONS

Markdown(app)

#===BEFORE/AFTER REQS===

@app.before_request
def before_request():

    session.permanent=True

    g.db=db_session()
    
    g.time=int(time.time())

    g.tor=request.headers.get("cf-ipcountry")=='T1'

    if "session_id" not in session:
        session["session_id"]=secrets.token_hex(16)

@app.after_request
def after_request(resp):

    #script nonce
    nonce=generate_hash(f"{session.get('session_id')}+{g.time}")
    
    resp.headers["Content-Security-Policy"] = f"default-src * data:; script-src 'self' hcaptcha.com code.jquery.com cdn.jsdelivr.net 'nonce-{nonce}'; object-src 'none'; style-src 'self'; media-src 'none';"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Permissions-Policy"] = "geolocation=(self)"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000"
    resp.headers["X-Content-Type-Options"]="nosniff"
    resp.headers["X-Frame-Options"]="DENY"

    if request.path.startswith("/assets/"):
        resp.headers["Cache-Control"]="public, max-age=604800"

    return resp
