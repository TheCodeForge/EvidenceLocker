from .mixins import *

import re
from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload
from evidencelocker.__main__ import Base

class BlogPost(Base, b36ids, time_mixin):

    __tablename__="blogs"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    created_utc =Column(Integer)
    author_id   =Column(Integer, ForeignKey("admin_users.id"))
    title       =Column(String(512))

    author = relationship("AdminUser", lazy="joined", back_populates="blogposts")


    @property
    def permalink(self):

        output = self.title.lower()

        output = re.sub('&\w{2,3};', '', output)

        output = [re.sub('\W', '', word) for word in output.split()]
        output = [x for x in output if x][0:6]

        output = '-'.join(output)

        if not output:
            output = '-'

        return f"/blog/{self.b36id}/{output}"