from evidencelocker.decorators.auth import *
from evidencelocker.__main__ import app

@app.get("/create_exhibit")
@logged_in_victim
def get_create_exhibit(user):

	return render_template(
		"create_exhibit.html",
		user=user
		)