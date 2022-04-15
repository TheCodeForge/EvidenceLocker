from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred
from sqlalchemy.ext.associationproxy import association_proxy

from .mixins import *

from evidencelocker.helpers.countries import COUNTRY_CODES
from evidencelocker.__main__ import Base

class VictimUser(Base, b36ids, time_mixin, user_mixin, json_mixin):

    __tablename__="victim_users"
    
    id          =Column(Integer, primary_key=True)
    username    =Column(String(64), unique=True)
    created_utc =Column(Integer)
    name        =Column(String(128))
    country_code=Column(String(2))
    created_country=Column(String(2))
    pw_hash     =deferred(Column(String(256)))
    otp_secret  =deferred(Column(String(32)))
    email       =Column(String(256), unique=True)
    banned_utc  =Column(Integer, default=None)
    ban_reason  =Column(String(128))
    login_nonce =Column(Integer, default=0)
    allow_leo_sharing = Column(Boolean, default=False)

    share_records = relationship("LockerShare")
    agencies = association+proxy('share_records', 'agency')

    def __repr__(self):
        return f'<VictimUser(id={self.id})>'
    
    @property
    def type_id(self):
        return f"v{self.id}"

    @property
    def permalink(self):
        return f"/locker/{self.username}"
    
    def can_be_viewed_by_user(self, other):

        if other is self:
            return True

        elif other.type_id.startswith("v"):
            return False

        elif other.type_id.startswith("a"):
            return True

        elif False: #replace with logic to identify police sharing:
            return True

        return False

    @property
    def signed_exhibit_count(self):
        return len([x for x in self.exhibits if x.signed_utc])

    @property
    def draft_exhibit_count(self):
        return len([x for x in self.exhibits if not x.signed_utc])

    @property
    def country(self):
        return COUNTRY_CODES.get(self.country_code)
    
    @property
    def json(self):
        data = super().json

        data["exhibits"]=[x.json_core for x in self.exhibits]

        return data
    