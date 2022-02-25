import time
import random
import werkzeug.security
import pyotp
from flask import *


from evidencelocker.__main__ import app

@app.post("/login_victim")
def login_victim():

	#define the response for an invalid login attempt
	#Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
	def invalid_login_victim():
		time.sleep(max(0, random.gauss(1.5, 0.33)))
		return redirect("/login_victim?invalid")

	user = get_victim_by_username(request.form.get("username"), graceful=True)
	if not user:
		return invalid_login_victim()

	if not werkzeug.security.check_password_hash(user.password_hash, request.form.get("password")):
		return invalid_login_victim()

	totp=pyotp.TOTP(user.otp_secret)
	if not totp.verify(request.form.get("otp_code")):
		return invalid_login_victim()

	#set cookie and continue to locker
	session["utype"]="v"
	session["uid"]=user.id

	return redirect("/locker")

@app.post("/login_police")
def login_police():

	#define the response for an invalid login attempt
	#Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
	def invalid_login_police():
		time.sleep(max(0, random.gauss(1.5, 0.33)))
		return redirect("/login_police?invalid")

	user = get_police_by_email(request.form.get("email"), graceful=True)
	if not user:
		return invalid_login_police()

	if not werkzeug.security.check_password_hash(user.password_hash, request.form.get("password")):
		return invalid_login_police()

	totp=pyotp.TOTP(user.otp_secret)
	if not totp.verify(request.form.get("otp_code")):
		return invalid_login_police()

	#set cookie and continue to lockers
	session["utype"]="p"
	session["uid"]=user.id

	return redirect("/lockers")

@app.post("/logout")
def logout():

	session.pop("utype")
	session.pop("uid")

	return redirect ("/")