from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload

from .mixins import time_mixin
from evidencelocker.__main__ import Base


class Entry(Base, time_mixin):

	__tablename__="entries"

    id          =Column(Integer, primary_key=True)