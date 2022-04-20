import bleach
import mistletoe
import pyotp
from pprint import pprint

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html, bleachify

from evidencelocker.__main__ import app


@app.get("/agency/<aid>/<anything>")
@logged_in_desired
def agency_aid_anything(user, aid, anything):


	agency = get_agency_by_id(aid)

	return render_template(
		"agency.html",
		a=agency,
		user=user)