from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload

from .mixins import time_mixin
from .victim import VictimUser
from .police import PoliceUser
from evidencelocker.__main__ import Base


class Exhibit(Base, time_mixin):

    __tablename__="entries"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    title       =Column(String(512))
    created_utc =Column(Integer)
    signed_utc  =Column(Integer)
    author_id   =Column(Integer, ForeignKey("victim_users.id"))

    author = relationship("Victim")

    @property
    @lazy
    def signed_string(self):
        return time.strftime("%d %B %Y at %H:%M:%S", time.gmtime(self.created_utc))


    def can_be_read_by_user(self, user):

        if isinstance(user, VictimUser) and user==self.author and not user.is_banned:

            return True

        elif isinstance(user, PoliceUser) and user.is_recently_verified and not user.is_banned:

            #if police belongs to agency that Vic has shared to:
            #    return True
            #else:
            #    return False
            pass

        elif isinstance(user, AdminUser) and not user.is_banned:

            return True

        return False