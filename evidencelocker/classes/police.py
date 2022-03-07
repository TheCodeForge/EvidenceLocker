from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred
import time

from .mixins import *
from evidencelocker.decorators.lazy import lazy
from evidencelocker.__main__ import Base

class PoliceUser(Base, time_mixin, user_mixin):
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
    last_verified_utc=Column(Integer, default=0)
    login_nonce =Column(Integer, default=0)

    agency      =relationship("Agency")

    
    @property
    def type_id(self):
        return f"p{self.id}"

    @property
    @lazy
    def is_recently_verified(self):
        return int(time.time()) - self.last_verified_utc < 60*60*24*14 #2 weeks
    