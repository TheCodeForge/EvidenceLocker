from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import *
from evidencelocker.__main__ import Base

class AdminUser(Base, b36ids, time_mixin, user_mixin):

    __tablename__="admin_users"
    
    id          =Column(Integer, primary_key=True)
    username    =Column(String(64), unique=True)
    created_utc =Column(Integer)
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =Column(String(32))
    email       =Column(String(256), unique=True)
    banned_utc  =Column(Integer, default=0)
    login_nonce =Column(Integer, default=0)
    last_otp_code = deferred(Column(String(6)))

    def __repr__(self):
        return f'<AdminUser(username="{self.username}")>'
    
    @property
    def type_id(self):
        return f"a{self.id}"

    @property
    def is_banned(self):
        return bool(self.banned_utc)

    @property
    def name(self):
        return self.username
    