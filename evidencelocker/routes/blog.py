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

@app.post("/blog")
@logged_in_admin
def post_blog_admin(user):

    title = bleachify(request.form.get("title"))

    body_raw = request.form.get("body")

    body_html = raw_to_html(body_raw)

    blog=BlogPost(
        title=title,
        text_raw=body_raw,
        text_html=body_html,
        created_utc=g.time,
        author_id=user.id
        )