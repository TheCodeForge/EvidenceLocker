from flask import *
from jinja2 import TemplateNotFound

from evidencelocker.__main__ import app

@app.errorhandler(401)
def error_401(e):
	return render_template("errors/401.html"), 401

@app.errorhandler(403)
def error_401(e):
	return render_template("errors/403.html"), 403

@app.errorhandler(404)
def error_401(e):
	return render_template("errors/404.html"), 404

@app.errorhandler(500)
def error_401(e):
	return render_template("errors/500.html"), 500

@app.errorhandler(TemplateNotFound)
def error_templatenotfound(e):
	return render_template("errors/404.html"), 404