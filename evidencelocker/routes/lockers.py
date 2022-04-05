from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html

from evidencelocker.__main__ import app

@app.get("/locker/<username>")
@app.get("/locker/<username>.json")
@logged_in_any
def get_locker_username(user, username):

	target_user = get_victim_by_username(username)

	if not target_user.can_be_viewed_by_user(user):
		abort(404)

	if request.path.endswith('.json'):
		return jsonify(target_user.json)

	return render_template(
		"victim_userpage.html",
		user=user,
		target_user=target_user
		)