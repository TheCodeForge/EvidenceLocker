from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload
import re
import werkzeug.security

from .mixins import *

from evidencelocker.decorators.lazy import lazy
from evidencelocker.__main__ import Base


class Exhibit(Base, b36ids, time_mixin, json_mixin):

    __tablename__="entries"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    title       =Column(String(512))
    created_utc =Column(Integer)
    edited_utc  =Column(Integer, default=None)
    signed_utc  =Column(Integer, default=None)
    author_id   =Column(Integer, ForeignKey("victim_users.id"))
    created_ip  =Column(String(16))
    edited_ip   =Column(String(16))
    signed_ip   =Column(String(16))
    created_country=Column(String(2))
    edited_country=Column(String(2))
    signed_country=Column(String(2))

    author = relationship("VictimUser", lazy="joined", backref="exhibits")

    def __repr__(self):
        return f'<Exhibit(id={self.id})>'
    
    def can_be_read_by_user(self, user):

        if user.type_id.startswith('v') and user==self.author and not user.is_banned:

            return True

        elif user.type_id.startswith('p') and user.is_recently_verified and not user.is_banned:

            if get_lockershare_by_exhibit_and_leo(self, user):
                return True

        elif user.type_id.startswith('a') and not user.is_banned:

            return True

        return False


    @property
    @lazy
    def permalink(self):

        output = self.title.lower()

        output = re.sub('&\w{2,3};', '', output)

        output = [re.sub('\W', '', word) for word in output.split()]
        output = [x for x in output if x][0:6]

        output = '-'.join(output)

        if not output:
            output = '-'

        return f"/locker/{self.author.username}/exhibit/{self.b36id}/{output}"

    @property
    @lazy
    def signed_string(self):
        return time.strftime("%d %B %Y at %H:%M:%S", time.gmtime(self.signed_utc)) if self.signed_utc else None

    @property
    @lazy
    def edited_string(self):
        return time.strftime("%d %B %Y at %H:%M:%S", time.gmtime(self.edited_utc)) if self.edited_utc else None

    @property
    def json(self):
        data = super().json

        data["author"]=self.author.json_core

        return data
    