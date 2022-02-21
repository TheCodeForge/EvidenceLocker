import sass
from flask import *

from evidencelocker.__main__ import app

@app.get("/assets/style/light.css")
def light_css():
	with open('evidencelocker/assets/style/light.scss') as stylesheet:
		return Response(
			sass.compile(string=stylesheet.read()),
			mimetype="text/css"
			)
