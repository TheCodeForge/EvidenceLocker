from evidencelocker.classes import *
from flask import *


def get_victim_by_username(name, graceful=False):

	if not isinstance(name, str):
		raise TypeError("Victim username must be str")

	user = g.db.query(Victim).filter_by(username=name).first()

	if not user and not graceful:
		abort(404)

	return user

def get_victim_by_id(id, graceful=False):

	if not isinstance(name, int):
		raise TypeError("ID must be int")

	user = g.db.query(Victim).filter_by(id=id).first()

	if not user and not graceful:
		abort(404)

	return user

def get_police_by_email(email, graceful=False):

	if not isinstance(email, str):
		raise TypeError("Police email must be str")

	user = g.db.query(Police).filter_by(email=name).first()

	if not user and not graceful:
		abort(404)

	return user
