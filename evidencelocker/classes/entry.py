from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload

from .mixins import time_mixin
from evidencelocker.__main__ import Base


class Entry(Base, time_mixin):

    __tablename__="entries"

    id          =Column(Integer, primary_key=True)
    text_raw    =Column(String(8192))
    text_html   =Column(String(16384))
    title       =Column(String(512))
    created_utc =Column(Integer)
    signed_utc  =Column(Integer)