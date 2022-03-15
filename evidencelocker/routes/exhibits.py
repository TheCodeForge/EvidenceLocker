import bleach
import mistletoe
import pyotp

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html

from evidencelocker.__main__ import app

@app.get("/create_exhibit")
@logged_in_victim
def get_create_exhibit(user):

    return render_template(
        "create_exhibit.html",
        user=user
        )

@app.post("/create_exhibit")
@logged_in_victim
def post_create_exhibit(user):

    title = request.form.get("title")

    body_raw = request.form.get("body")

    body_html = raw_to_html(body_raw)

    signed = request.form.get("oath_perjury", False)

    if signed:
        if not werkzeug.security.check_password_hash(user.pw_hash, request.form.get("password")) or not pyotp.TOTP(user.otp_secret).verify(request.form.get("otp_code")):
            return render_template(
                "create_exhibit.html",
                user=user,
                error="Invalid signature",
                title=title,
                body=body_raw
                )

    exhibit = Exhibit(
        text_raw=body_raw,
        text_html=body_html,
        title=title,
        created_utc=g.time,
        signed_utc=g.time if signed else 0,
        author_id=user.id
        )
    g.db.add(exhibit)
    g.db.commit()
    return redirect(exhibit.permalink)

@app.get("/locker/<username>/exhibit/<eid>/<anything>")
@logged_in_any
def get_locker_username_exhibit_eid_anything(user, username, eid, anything):

    exhibit = get_exhibit_by_id(eid)

    if not exhibit.can_be_read_by_user(user):
        abort(404)

    return render_template(
        "exhibit_page.html",
        e=exhibit,
        user=user
        )