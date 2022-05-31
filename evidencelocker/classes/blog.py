from .mixins import *

from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload
from evidencelocker.__main__ import Base

class BlogEntry(Base, b36ids, time_mixin):

    __tablename__="blogs"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    created_utc =Column(Integer)
    author_id   =Column(Integer)


    author = relationship("AdminUser", lazy="joined", back_populates="blogposts")