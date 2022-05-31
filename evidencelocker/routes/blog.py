from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html, bleachify
from evidencelocker.helpers.loaders import *

from evidencelocker.__main__ import app

@app.get("/blog/<bid>/<anything>")
@logged_in_desired
def get_blog_bid_anything(user, bid, anything):

	blog = get_blog_by_id(bid)

	return render_template(
		"blog.html",
		user=user,
		b=blog
		)