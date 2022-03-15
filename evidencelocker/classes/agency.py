from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload, deferred

from .mixins import *
from evidencelocker.__main__ import Base

class Agency(Base, b36ids, time_mixin):

	__tablename__="agencies"

	id=Column(Integer, primary_key=True)
	name=Column(String(256), unique=True)
	city=Column(String(128))
	state=Column(String(128))
	country=Column(String(2))
	domain=Column(String(128), unique=True)


class BadDomain(Base):

	__tablename__="bad_domains"

	id=Column(Integer, primary_key=True)
	domain=Column(String(128), unique=True)