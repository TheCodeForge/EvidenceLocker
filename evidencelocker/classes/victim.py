from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred
from sqlalchemy.ext.associationproxy import association_proxy

from .mixins import *

from evidencelocker.helpers.countries import COUNTRY_CODES, RESTRICTED_COUNTRIES
from evidencelocker.helpers.hashes import validate_hash
from evidencelocker.__main__ import Base

class VictimUser(Base, b36ids, time_mixin, user_mixin, json_mixin, country_mixin):

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
    banned_utc  =Column(Integer, default=0)
    ban_reason  =Column(String(128))
    login_nonce =Column(Integer, default=0)
    allow_leo_sharing = Column(Boolean, default=False)
    last_otp_code = deferred(Column(String(6)))

    share_records = relationship("LockerShare", back_populates="victim")
    agencies = association_proxy('share_records', 'agency')

    exhibits = relationship("Exhibit", order_by="Exhibit.id.desc()", back_populates="author")

    def __repr__(self):
        return f'<VictimUser(id={self.id})>'
    
    @property
    def type_id(self):
        return f"v{self.id}"

    @property
    def permalink(self):
        return f"/locker/{self.username}"
    
    def can_be_viewed_by_user(self, other):

        if not other:
            return False

        if other.is_banned:
            return False

        if other is self:
            return True

        elif other.type_id.startswith("v"):
            return False

        elif other.type_id.startswith("a"):
            return True

        elif other.type_id.startswith("p"):

            if not other.is_recently_verified:
                return False
                
            if self.allow_leo_sharing and other.agency.country_code==self.country_code and self.country_code not in RESTRICTED_COUNTRIES:
                return True

            elif other.agency_id in [x.agency_id for x in self.share_records]:
                return True

            return False

        return validate_hash(request.path, request.args.get("token",""))

    @property
    def signed_exhibit_count(self):
        return len([x for x in self.exhibits if x.signed_utc])

    @property
    def draft_exhibit_count(self):
        return len([x for x in self.exhibits if not x.signed_utc])
    
    @property
    def json(self):
        data = super().json

        data["exhibits"]=[x.json_core for x in self.exhibits]

        return data