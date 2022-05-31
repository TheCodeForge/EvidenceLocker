from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html, bleachify
from evidencelocker.helpers.loaders import *

from evidencelocker.__main__ import app

@app.get("/blog/<bid>/<anything>")
@logged_in_desired
def get_blog_bid_anything(user, bid, anything):

    blog = get_blog_by_id(bid)

    return render_template(
        "blog_page.html",
        user=user,
        b=blog
        )

@app.get("/blog")
@logged_in_desired
def get_blogs(user):

    page=max(0, int(request.args.get("page", 1)))

    blogs=g.db.query(BlogPost).order_by(BlogPost.id.desc()).offset(25*(page-1)).limit(25).all()

    return render_template(
        "blogs.html",
        user=user,
        listing=blogs
        )



@app.get("/create_blog")
@logged_in_admin
def get_create_blog(user):
    return render_template(
        "admin/edit_blog.html",
        user=user)

@app.post("/create_blog")
@logged_in_admin
@validate_csrf_token
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

    g.db.add(blog)
    g.db.commit()
    return redirect(blog.permalink)

@app.get("/edit_blog/<bid>")
@logged_in_admin
def get_blog_edit_bid(user, bid):

    blog = get_blog_by_id(bid)

    return render_template(
        "admin/edit_blog.html",
        user=user,
        b=blog
        )

@app.post("/edit_blog/<bid>")
@logged_in_admin
@validate_csrf_token
def post_edit_blog_bid(user, bid):

    blog = get_blog_by_id(bid)

    blog.title = bleachify(request.form.get("title"))
    blog.text_raw = request.form.get("body")
    blog.text_html = raw_to_html(blog.text_raw)

    g.db.add(blog)
    g.db.commit()
    return redirect(blog.permalink)