from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import *
from evidencelocker.__main__ import Base

class VictimUser(Base, time_mixin, user_mixin):

    __tablename__="victim_users"
    
    id          =Column(Integer, primary_key=True)
    username    =Column(String(64))
    created_utc =Column(Integer)
    name        =Column(String(128))
    country     =Column(String(2))
    created_country=Column(String(2))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256))
    banned_utc  =Column(Integer, default=0)
    login_nonce =Column(Integer, default=0)
    
    @property
    def type_id(self):
        return f"v{self.id}"

