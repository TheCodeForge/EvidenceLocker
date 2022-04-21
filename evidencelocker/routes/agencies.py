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

	if request.path != agency.permalink:
		return redirect(agency.permalink)

	share = get_lockershare_by_agency(user, agency)

	return render_template(
		"agency.html",
		a=agency,
		user=user,
		shared = bool(share)
		)

@app.post("/agency/<aid>/<anything>")
@logged_in_victim
@validate_csrf_token
def post_agency_aid_anything(user, aid, anything):

	#create sharing record

	agency = get_agency_by_id(aid)

	existing_record = get_lockershare_by_agency(victim, agency)

	if existing_record:
		abort(409)

	share_record = LockerShare(
		agency_id=agency.id,
		victim_id=user.id,
		created_utc=g.time
		)

	g.db.add(share_record)

	g.db.commit()

	return redirect(agency.permalink)