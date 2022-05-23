import bleach
import mistletoe
import pyotp
from pprint import pprint
import random

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.hashes import *
from evidencelocker.helpers.text import raw_to_html, bleachify

from evidencelocker.__main__ import app

@app.get("/login_admin")
@logged_in_desired
def get_login_admin(user):

    if user:
        return redirect("/")

    return render_template(
        "login_admin.html",
        token=logged_out_csrf_token()
        )

@app.post("/login_admin")
def post_login_admin():

    #define the response for an invalid login attempt
    #Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
    def invalid_login_admin(error=None):
        time.sleep(max(0, random.gauss(1.5, 0.33)))
        return render_template(
            "login_admin.html",
            token=logged_out_csrf_token(),
            error=error
            )

    user = get_admin_by_username(request.form.get("username"), graceful=True)
    if not user:
        return invalid_login_admin("Invalid username, password, or two-factor code")

    if not user.validate_password(request.form.get("password")):
        return invalid_login_admin("Invalid username, password, or two-factor code")

    if not user.validate_otp(request.form.get("otp_code"), allow_reset=True):
        return invalid_login_admin("Invalid username, password, or two-factor code")

    #set cookie and continue to locker
    session["utype"]="a"
    session["uid"]=user.id

    return redirect("/")

@app.post("/locker/<username>/ban")
@app.post("/locker/<username>/unban")
@logged_in_admin
@validate_csrf_token
def locker_username_ban_x(user, username):

	target_user=get_victim_by_username(username)

	if request.path.endswith("/ban"):
		target_user.banned_utc=g.time
		target_user.ban_reason = bleachify(request.form.get("ban_reason",""))

	elif request.path.endswith("/unban"):
		target_user.banned_utc=0

	g.db.add(target_user)
	g.db.commit()
	return redirect(target_user.permalink)

@app.get("/agency")
@app.get("/agency/<aid>/<anything>/edit")
@logged_in_admin
def get_agency(user, aid=None, anything=None):

    agency= get_agency_by_id(aid) if aid else None

    return render_template(
        "admin/edit_agency.html",
        a=agency,
        user=user
        )

@app.post("/agency")
@logged_in_admin
@validate_csrf_token
def post_agency(user):

    #create agency

    agency=Agency(
        name=           bleachify(request.form.get("name")),
        city=           bleachify(request.form.get("city")),
        state=          bleachify(request.form.get("state")),
        country_code=   request.form.get("cc"),
        domain=         bleachify(request.form.get("domain")),
        site=           bleachify(request.form.get("site"))
        )

    g.db.add(agency)
    g.db.commit()

    #apply agency link to appropriate LEO accounts
    #search by email domain

    users = g.db.query(PoliceUser).filter(PoliceUser.domain.ilike(f"%@{agency.domain}")).all()
    for user in users:
        user.agency_id=agency.id
        g.db.add(user)

    g.db.commit()


    return redirect(agency.permalink)

@app.post("/agency/<aid>/<anything>")
@logged_in_admin
@validate_csrf_token
def post_agency_aid_anything(user, aid, anything):

    #edit agency

    a=get_agency_by_id(aid)

    a.name=           bleachify(request.form.get("name")),
    a.city=           bleachify(request.form.get("city")),
    a.state=          bleachify(request.form.get("state")),
    a.country_code=   bleachify(request.form.get("cc")),
    a.site=           bleachify(request.form.get("site"))

    g.db.add(a)
    g.db.commit()

    return redirect(a.permalink)


@app.get("/users/police/unverified")
@logged_in_admin
def users_police_unverified(user):

    listing = g.db.query(PoliceUser).filter_by(agency_id=None).all()

    return render_template(
        "admin/police.html",
        user=user,
        listing=listing
        )

@app.get("/police/<pid>")
@logged_in_admin
def get_police_pid_admin(user, pid):

    police=get_police_by_id(pid)

    victims=g.db.query(VictimUser).filter(
        or_(
            and_(
                VictimUser.country_code==police.agency.country_code,
                VictimUser.allow_leo_sharing==True
                ),
            VictimUser.id.in_(
                g.db.query(LockerShare.victim_id).filter(LockerShare.agency_id==police.agency_id).subquery()
                )
            )
        ).all() if police.agency else []

    return render_template(
        "police_home.html",
        user=user,
        listing=victims,
        target_user=police
        )

@app.post("/police/<pid>/ban")
@app.post("/police/<pid>/unban")
@logged_in_admin
@validate_csrf_token
def police_pid_ban_unban(user, pid):

    target_user=get_police_by_id(pid)

    if request.path.endswith("/ban"):
        target_user.banned_utc=g.time
        target_user.ban_reason = bleachify(request.form.get("ban_reason",""))

    elif request.path.endswith("/unban"):
        target_user.banned_utc=0

    g.db.add(target_user)
    g.db.commit()
    return redirect(target_user.permalink)