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
app.config['DATABASE_URL']                  = environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
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

from .classes import *
from .routes import *

#===ALEMBIC DB SCHEMA UPDATE===
from alembic.config import Config
from alembic import command
#LOG.info('Running DB migrations in %r on %r', script_location, dsn)
alembic_cfg = Config()
#alembic_cfg.set_main_option('sqlalchemy.url', app.config["DATABASE_URL"])
alembic_cfg.set_main_option('script_location',  "/alembic")
#alembic_cfg.attributes['target_metadata']=Base.metadata
command.revision(alembic_cfg, autogenerate=True)
command.upgrade(alembic_cfg, 'head')

@app.before_request
def before_request():

    session.permanent=True

@app.get('/')
def home():
    return render_template(
        "base.html"
        )