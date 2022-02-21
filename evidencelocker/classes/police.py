from sqlalchemy import *

from evidencelocker.__main__ import Base

class PoliceUser(Base):
	__tablename__="police_users"
	
	id          =Column(Integer, primary_key=True)
	name 		=Column(String(256))