from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred
from sqlalchemy.ext.associationproxy import association_proxy
import time

from .mixins import *
from evidencelocker.decorators.lazy import lazy
from evidencelocker.__main__ import Base

class PoliceUser(Base, b36ids, time_mixin, user_mixin):
    __tablename__="police_users"
    
    id          =Column(Integer, primary_key=True)
    name        =Column(String(256))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256), unique=True)
    agency_id   =Column(Integer, ForeignKey('agencies.id'))
    banned_utc  =Column(Integer, default=0)
    ban_reason  =Column(String(128))
    last_verified_utc=Column(Integer, default=0)
    login_nonce =Column(Integer, default=0)
    created_utc =Column(Integer)

    agency      =relationship("Agency")

    share_records = relationship(
        "LockerShare", 
        primaryjoin = "PoliceUser.agency_id==LockerShare.agency_id",
        foreign_keys = agency_id,
        viewonly=True
        )
    victims = association_proxy("share_records", "victim")

    def __repr__(self):
        return f'<PoliceUser(id={self.id})>'

    
    @property
    def type_id(self):
        return f"p{self.id}"

    @property
    def username(self):
        return self.email

    @property
    @lazy
    def is_recently_verified(self):
        return int(time.time()) - self.last_verified_utc < 60*60*24*14 #2 weeks
    