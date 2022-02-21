import sass
from flask import *

from evidencelocker.__main__ import app

@app.get('/')
def home():
    return render_template(
        "home.html"
        )

@app.get("/help/<pagename>")
def help(pagename):
	return render_template(safe_join("/help", pagename)+'.html')

@app.get("/assets/style/light.css")
def light_css():
	with open('evidencelocker/assets/style/light.scss') as stylesheet:
		return Response(
			sass.compile(string=stylesheet.read()),
			mimetype="text/css"
			)
