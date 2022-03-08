from .b36 import *
from flask import *
from evidencelocker.classes import *


def get_victim_by_username(name, graceful=False):

	if not isinstance(name, str):
		raise TypeError("Victim username must be str")

	user = g.db.query(VictimUser).filter_by(username=name).first()

	if not user and not graceful:
		abort(404)

	return user

def get_victim_by_id(id, graceful=False):

	if isinstance(id, str):
		id=base36decode(id)

	user = g.db.query(VictimUser).filter_by(id=id).first()

	if not user and not graceful:
		abort(404)

	return user

def get_police_by_email(email, graceful=False):

	if not isinstance(email, str):
		raise TypeError("Police email must be str")

	user = g.db.query(PoliceUser).filter_by(email=name).first()

	if not user and not graceful:
		abort(404)

	return user


def get_police_by_id(id, graceful=False):

	if isinstance(id, str):
		id=base36decode(id)

	user = g.db.query(PoliceUser).filter_by(id=id).first()

	if not user and not graceful:
		abort(404)

	return user


def get_admin_by_id(id, graceful=False):

	if isinstance(id, str):
		id=base36decode(id)

	user = g.db.query(AdminUser).filter_by(id=id).first()

	if not user and not graceful:
		abort(404)

	return user

def get_exhibit_by_id(id, graceful=False):

	if isinstance(id, str):
		id=base36decode(id)

	exhibit = g.db.query(Exhibit).filter_by(id=id).first()

	if not exhibit and not graceful:
		abort(404)

	return exhibit

