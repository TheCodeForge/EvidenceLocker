from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload
import re
import werkzeug.security

from .mixins import *

from evidencelocker.decorators.lazy import lazy
from evidencelocker.__main__ import Base


class Exhibit(Base, b36ids, time_mixin):

    __tablename__="entries"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    title       =Column(String(512))
    created_utc =Column(Integer)
    signed_utc  =Column(Integer)
    author_id   =Column(Integer, ForeignKey("victim_users.id"))

    author = relationship("VictimUser")    


    def can_be_read_by_user(self, user):

        if user.type_id.startswith('v') and user==self.author and not user.is_banned:

            return True

        elif user.type_id.startswith('p') and user.is_recently_verified and not user.is_banned:

            #if police belongs to agency that Vic has shared to:
            #    return True
            #else:
            #    return False
            pass

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
        return time.strftime("%d %B %Y at %H:%M:%S", time.gmtime(self.created_utc)) if self.signed_utc else None