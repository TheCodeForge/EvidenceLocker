from sqlalchemy import *
from sqlalchemy.orm import relationship, lazyload

from evidencelocker.__main__ import Base

class VictimUser(Base):

    __tablename__="victim_users"
    
    id          =Column(Integer, primary_key=True)
    created_utc =Column(Integer)