from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import time_mixin
from evidencelocker.__main__ import Base

class Agency(Base, time_mixin):

	__tablename__="agencies"

	id=Column(Integer, primary_key=True)
	name=Column(String(256))
	country=Column(String(2))
	domain=Column(String(128))