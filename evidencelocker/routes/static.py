import sass
from flask import *
from werkzeug.utils import safe_join

from evidencelocker.decorators.auth import *
from evidencelocker.__main__ import app

@app.get('/')
@logged_in_desired
def home(user):
    if user and user.type_id.startswith('v'):
        return redirect(user.permalink)

    elif user and user.type_id.startswith('p'):
        return redirect("/locker")

    #elif user and user.type_id.startswith('a'):
    #    return redirect("/admin_dashboard")

    blogs=g.db.query(BlogPost).order_by(BlogPost.id.desc()).limit(3)

    return render_template(
        "home.html",
        user=user,
        blogs=blogs
        )

@app.get("/help/<pagename>")
@logged_in_desired
def help(user, pagename):
    
    return render_template(
        safe_join("/help", pagename)+'.html',
        user=user
        )

@app.get("/assets/style/<stylefile>.css")
def light_css(stylefile):
    with open(safe_join("evidencelocker/assets/style/", stylefile)+'.scss') as stylesheet:
        return Response(
            sass.compile(string=stylesheet.read()),
            mimetype="text/css"
            )

@app.post("/toggle_darkmode")
def post_toggle_darkmode():
    session["darkmode"] = not session.get('darkmode', False)
    return "", 201