import sass
from flask import *

from evidencelocker.decorators.auth import *
from evidencelocker.__main__ import app

@app.get('/')
@logged_in_desired
def home(user):
    return render_template(
        "home.html",
        user=user
        )

@app.get("/help/<pagename>")
@logged_in_desired
def help(pagename):
	return render_template(
		safe_join("/help", pagename)+'.html',
		user=user
		)

@app.get("/assets/style/light.css")
def light_css():
	with open('evidencelocker/assets/style/light.scss') as stylesheet:
		return Response(
			sass.compile(string=stylesheet.read()),
			mimetype="text/css"
			)
