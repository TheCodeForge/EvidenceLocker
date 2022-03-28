import bleach
import mistletoe
import pyotp

from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html

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
        user.country_code=request.form.get("country_code") or user.country_code

    elif page=="security":
        pass

    else:
        abort(404)

    g.db.add(user)
    g.db.commit()

    return '', 201