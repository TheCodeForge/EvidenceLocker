import bleach
import mistletoe
import pyotp
from werkzeug.utils import safe_join

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html
from evidencelocker.helpers.countries import COUNTRY_CODES

from evidencelocker.__main__ import app


@app.get("/settings")
@logged_in_victim
def get_settings(user):
    return redirect("/settings/profile")


@app.get("/settings/<page>")
@logged_in_victim
def get_settings_page(user, page):

    return render_template(
        f"{safe_join('settings/', page)}.html",
        user=user
        )

@app.post("/settings/<page>")
@logged_in_victim
@validate_csrf_token
def post_settings_page(user, page):

    if page=="profile":


        user.name=request.form.get("name") or user.name

        if request.form.get("country_code")!=user.country_code:
            if request.form.get("country_code") not in COUNTRY_CODES:
                return jsonify({"error":"Invalid country selection"}), 400
            user.allow_leo_sharing=False
            user.country_code=request.form.get("country_code") or user.country_code

    elif page=="security":
        


        if request.form.get("function")=="pw_reset":

            if not user.validate_password(request.form.get("password")) or not user.validate_otp(request.form.get("otp_code")):
                return jsonify({'error':'Invalid password or two-factor code.'}), 401

            if request.form.get("new_pw") != request.form.get("confirm_pw"):
                return jsonify({'error': "Passwords don't match"}), 400

            user.pw_hash = werkzeug.security.generate_password_hash(request.form.get("password"))

        elif request.form.get("function")=="otp_reset":

            if not user.validate_password(request.form.get("password")) or not user.validate_otp(request.form.get("otp_code"), allow_reset=True):
                return jsonify({'error':'Invalid password or two-factor code.'}), 401

            user.otp_secret=None
            g.db.add(user)
            g.db.commit()
            return redirect("/set_otp")

    elif page=="sharing":

        if request.form.get("function")=="toggle_sharing":
            user.allow_leo_sharing=bool(request.form.get("allow_sharing", False))

        elif request.form.get("function")=="revoke_public":
            user.public_link_nonce +=1
            g.db.add(user)
            g.db.commit()
            return jsonify({"message":"Public links revoked"})

    else:
        abort(404)

    g.db.add(user)
    g.db.commit()

    return jsonify({"message": "Settings updated"})