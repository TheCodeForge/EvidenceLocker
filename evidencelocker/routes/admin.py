import bleach
import mistletoe
import pyotp
from pprint import pprint

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.hashes import *
from evidencelocker.helpers.text import raw_to_html, bleachify

from evidencelocker.__main__ import app

@app.get("/login_admin")
@logged_in_desired
def get_login_admin(user):

    if user:
        return redirect("/")

    return render_template(
        "login_admin.html",
        token=logged_out_csrf_token()
        )

@app.post("/login_admin")
def post_login_admin():

    #define the response for an invalid login attempt
    #Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
    def invalid_login_admin(error=None):
        time.sleep(max(0, random.gauss(1.5, 0.33)))
        return render_template(
            "login_victim.html",
            token=logged_out_csrf_token(),
            error=error
            )

    user = get_admin_by_username(request.form.get("username"), graceful=True)
    if not user:
        return invalid_login_admin("Invalid username, password, or two-factor code")

    if not user.validate_password(request.form.get("password")):
        return invalid_login_admin("Invalid username, password, or two-factor code")

    if not user.validate_otp(request.form.get("otp_code"), allow_reset=True):
        return invalid_login_admin("Invalid username, password, or two-factor code")

    #set cookie and continue to locker
    session["utype"]="a"
    session["uid"]=user.id

    return redirect("/")

app.post("/locker/<username>/ban/<x>")
@logged_in_admin
@validate_csrf_token
def locker_username_ban_x(user, username, x):

	target_user=get_victim_by_username(username)

	if x=="1":
		target_user.banned_utc=g.time
		target_user.ban_reason = bleachify(request.form.get("ban_reason",""))

	elif x=="0":
		target_user.banned_utc=0

	else:
		abort(404)

	g.db.add(target_user)
	g.db.commit()
	return redirect(target_user.permalink)