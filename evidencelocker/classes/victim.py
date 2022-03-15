from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import *
from evidencelocker.__main__ import Base

class VictimUser(Base, b36ids, time_mixin, user_mixin):

    __tablename__="victim_users"
    
    id          =Column(Integer, primary_key=True)
    username    =Column(String(64), unique=True)
    created_utc =Column(Integer)
    name        =Column(String(128))
    country     =Column(String(2))
    created_country=Column(String(2))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256), unique=True)
    banned_utc  =Column(Integer, default=0)
    ban_reason  =Column(String(128))
    login_nonce =Column(Integer, default=0)
    
    @property
    def type_id(self):
        return f"v{self.id}"

    @property
    def permalink(self):
        return f"/locker/{self.username}"
    