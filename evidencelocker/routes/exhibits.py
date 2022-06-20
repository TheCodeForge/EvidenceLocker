import bleach
import mistletoe
import pyotp
from pprint import pprint

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html, bleachify
from evidencelocker.helpers.aws import s3_upload_file, s3_download_file

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

    title = bleachify(request.form.get("title"))

    body_raw = request.form.get("body")

    body_html = raw_to_html(body_raw)

    signed = request.form.get("oath_perjury", False)

    if signed:
        if not user.validate_password(request.form.get("password")) or not user.validate_otp(request.form.get("otp_code")):
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
        author_id=user.id,
        created_country = request.headers.get("cf-ipcountry"),
        created_ip  = request.remote_addr
        )



    g.db.add(exhibit)
    g.db.flush()
    g.db.refresh(exhibit)

    if "file" in request.files:
        file=request.files["file"]
        if file.filename:
            s3_upload_file(f"{exhibit.b36id}.png", file)


    if signed:
        exhibit.signed_ip = request.remote_addr
        exhibit.signed_country  = request.headers.get("cf-ipcountry")
        exhibit.signed_utc=g.time
        g.db.add(exhibit)
        g.db.commit()
        g.db.refresh(exhibit)
        exhibit.signing_sha256 = exhibit.live_sha256

    g.db.commit()
    return redirect(exhibit.permalink)

@app.get("/locker/<username>/exhibit/<eid>/<anything>")
@app.get("/locker/<username>/exhibit/<eid>/<anything>.json")
@logged_in_any
def get_locker_username_exhibit_eid_anything(user, username, eid, anything):

    exhibit = get_exhibit_by_id(eid)

    if not exhibit.author.can_be_viewed_by_user(user):
        abort(404)

    if username != exhibit.author.username:
        abort(404)

    if request.path != exhibit.permalink and request.path != exhibit.jsonlink:
        return redirect(exhibit.permalink)

    if request.path.endswith(".json"):
        return jsonify(exhibit.json)

    return render_template(
        "exhibit_page.html",
        e=exhibit,
        user=user
        )

@app.get("/locker/<username>/exhibit/<eid>/<anything>/signature")
@logged_in_any
def get_locker_username_exhibit_eid_anything_signature(user, username, eid, anything):

    exhibit = get_exhibit_by_id(eid)

    if not exhibit.author.can_be_viewed_by_user(user):
        abort(404)

    if username != exhibit.author.username:
        abort(404)

    if request.path != exhibit.sig_permalink:
        return redirect(exhibit.sig_permalink)

    if not exhibit.signed_utc:
        return redirect(exhibit.permalink)

    return render_template(
        "exhibit_sig.html",
        e=exhibit,
        user=user
        )

@app.get("/edit_exhibit/<eid>")
@logged_in_victim
def get_edit_exhibit_eid(user, eid):

    exhibit = get_exhibit_by_id(eid)

    if exhibit.author != user:
        abort(404)

    if exhibit.signed_utc:
        return redirect(exhibit.permalink)

    return render_template(
        "create_exhibit.html",
        user=user,
        e=exhibit
        )

@app.post("/edit_exhibit/<eid>")
@logged_in_victim
def post_edit_exhibit_eid(user, eid):

    exhibit = get_exhibit_by_id(eid)

    if exhibit.author != user:
        abort(404)

    if exhibit.signed_utc:
        abort(403)


    signed = request.form.get("oath_perjury", False)

    if signed:
        if not user.validate_password(request.form.get("password")) or not user.validate_otp(request.form.get("otp_code")):
            return render_template(
                "create_exhibit.html",
                user=user,
                error="Invalid signature",
                e=exhibit
                )


    title = bleachify(request.form.get("title"))

    body_raw = request.form.get("body").replace('\r', '')

    body_html = raw_to_html(body_raw)

    edited = (body_raw != exhibit.text_raw or title != exhibit.title)

    exhibit.edited_utc = g.time if edited else exhibit.edited_utc
    exhibit.edited_ip = request.remote_addr if edited else exhibit.edited_ip
    exhibit.edited_country = request.headers.get("cf-ipcountry") if edited else exhibit.edited_country
    exhibit.signed_utc = g.time if signed else exhibit.signed_utc
    exhibit.signed_ip = request.remote_addr if signed else None
    exhibit.signed_country = request.headers.get("cf-ipcountry") if signed else None
    exhibit.text_raw = body_raw
    exhibit.text_html = body_html
    exhibit.title = title

    exhibit.signing_sha256 = exhibit.live_sha256 if signed else None

    g.db.add(exhibit)
    g.db.commit()

    return redirect(exhibit.permalink)


@app.get("/exhibit_image/<eid>.png")
@logged_in_any
def get_exhibit_image_eid_png(user, eid):

    exhibit = get_exhibit_by_id(eid)

    if not exhibit.author.can_be_viewed_by_user(user):
        abort(404)

    b=s3_download_file(f"{eid}.png")

    resp=make_response(b)
    b.headers["Content-Type"]="image/png"
    return resp
