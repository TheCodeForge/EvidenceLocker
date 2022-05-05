from evidencelocker.decorators.auth import *
from evidencelocker.helpers.text import raw_to_html

from evidencelocker.classes import *
from evidencelocker.__main__ import app

@app.get("/locker/<username>")
@app.get("/locker/<username>.json")
@logged_in_any
def get_locker_username(user, username):

    target_user = get_victim_by_username(username)

    if not target_user.can_be_viewed_by_user(user):
        abort(404)

    if request.path.endswith('.json'):
        return jsonify(target_user.json)

    return render_template(
        "victim_userpage.html",
        user=user,
        target_user=target_user
        )

@app.get("/locker")
@logged_in_police
def get_lockers_leo(user):

    victims = g.db.query(VictimUser).filter(
        or_(
            and_(
                VictimUser.country_code==user.agency.country_code,
                VictimUser.allow_leo_sharing==True
                ),
            VictimUser.id.in_(
                g.db.query(LockerShare.victim_id).filter(LockerShare.agency_id==user.agency_id).subquery()
                )
            )
        ).all()

    return render_template(
        "police_home.html",
        user=user,
        listing=victims
        )