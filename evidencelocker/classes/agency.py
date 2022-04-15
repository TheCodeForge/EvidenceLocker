import re
from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred
from sqlalchemy.ext.associationproxy import association_proxy

from .mixins import *
from evidencelocker.helpers.countries import COUNTRY_CODES
from evidencelocker.__main__ import Base

class Agency(Base, b36ids, time_mixin):

    __tablename__="agencies"

    id=Column(Integer, primary_key=True)
    name=Column(String(256), unique=True)
    city=Column(String(128))
    state=Column(String(128))
    country_code=Column(String(2), index=True)
    domain=Column(String(128), unique=True)

    share_records = relationship("LockerShare")
    victims = association_proxy("share_records", "victim")

    def __repr__(self):
        return f'<Agency(id={self.id})>'

    @property
    def country(self):
        return COUNTRY_CODES[self.country_code]

    @property
    @lazy
    def permalink(self):

        output = self.name.lower()

        output = re.sub('&\w{2,3};', '', output)

        output = [re.sub('\W', '', word) for word in output.split()]
        output = [x for x in output if x][0:6]

        output = '-'.join(output)

        if not output:
            output = '-'

        return f"/agency/{self.b36id}/{output}"
    


class BadDomain(Base):

    __tablename__="bad_domains"

    id=Column(Integer, primary_key=True)
    domain=Column(String(128), unique=True)

    def __repr__(self):
        return f'<BadDomain(domain={self.domain})>'

class LockerShare(Base, time_mixin):

    __tablename__="locker_shares"

    id=Column(Integer, primary_key=True)
    agency_id=Column(Integer, ForeignKey("agencies.id"))
    victim_id=Column(Integer, ForeignKey("victim_users.id"))
    created_utc=Column(Integer)

    victim=relationship("VictimUser", lazy="joined")
    agency=relationship("Agency")