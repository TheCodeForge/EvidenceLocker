from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import time_mixin
from evidencelocker.__main__ import Base

class VictimUser(Base, time_mixin):

    __tablename__="victim_users"
    
    id          =Column(Integer, primary_key=True)
    username    =Column(String(64))
    created_utc =Column(Integer)
    name        =Column(String(128))
    country     =Column(String(2))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256))


