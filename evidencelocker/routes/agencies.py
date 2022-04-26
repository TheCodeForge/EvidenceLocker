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

	existing_record = get_lockershare_by_agency(user, agency)

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

@app.get("/search_agencies")
@logged_in_desired
def get_agency_country_cc(user):

	cc=request.args.get("cc", None)
	name=request.args.get("name", None)

	agencies = g.db.query(Agency)

	if cc:
		agencies=agencies.filter_by(country_code=cc.upper())

	if name:
		words=name.split()
        words=[Agency.name.ilike('%'+x+'%') for x in words]
        words=tuple(words)
        agencies=agencies.filter(*words)


	agencies=agencies.order_by(Agency.name.asc()).all()

	return render_template(
		"search_agencies.html",
		listing=agencies,
		user=user
		)