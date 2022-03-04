from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import time_mixin
from evidencelocker.__main__ import Base

class PoliceUser(Base, time_mixin):
    __tablename__="police_users"
    
    id          =Column(Integer, primary_key=True)
    name        =Column(String(256))
    username    =Column(String(64))
    created_utc =Column(Integer)
    name        =Column(String(128))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256))
    agency_id   =Column(Integer, ForeignKey('agencies.id'))
    banned_utc  =Column(Integer, default=0)

    agency      =relationship("Agency")
    
    @property
    def is_banned(self):
        return bool(self.banned_utc)
