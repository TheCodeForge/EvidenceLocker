import bleach
import mistletoe
import pyotp
from pprint import pprint

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html, bleachify

from evidencelocker.__main__ import app

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