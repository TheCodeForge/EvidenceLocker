from .b36 import *
from flask import *
from evidencelocker.classes import *


def get_victim_by_username(name, graceful=False):

    if not isinstance(name, str):
        raise TypeError("Victim username must be str")

    name = name.replace('\\', '')
    name = name.replace('_', '\_')
    name = name.replace('%', '')

    user = g.db.query(VictimUser).filter(VictimUser.username.ilike(name)).first()

    if not user and not graceful:
        abort(404)

    return user

def get_victim_by_id(id, graceful=False):

    if isinstance(id, str):
        id=base36decode(id)

    user = g.db.query(VictimUser).filter_by(id=id).first()

    if not user and not graceful:
        abort(404)

    return user

def get_police_by_email(email, graceful=False):

    if not isinstance(email, str):
        raise TypeError("Police email must be str")

    email = email.replace('\\', '')
    email = email.replace('_', '\_')
    email = email.replace('%', '')

    user = g.db.query(PoliceUser).filter(PoliceUser.email.ilike(email)).first()

    if not user and not graceful:
        abort(404)

    return user


def get_police_by_id(id, graceful=False):

    if isinstance(id, str):
        id=base36decode(id)

    user = g.db.query(PoliceUser).filter_by(id=id).first()

    if not user and not graceful:
        abort(404)

    return user


def get_admin_by_id(id, graceful=False):

    if isinstance(id, str):
        id=base36decode(id)

    user = g.db.query(AdminUser).filter_by(id=id).first()

    if not user and not graceful:
        abort(404)

    return user

def get_admin_by_username(name, graceful=False):

    user = g.db.query(AdminUser).filter_by(username=name).first()

    if not user and not graceful:
        abort(404)

    return user

def get_exhibit_by_id(id, graceful=False):

    if isinstance(id, str):
        id=base36decode(id)

    exhibit = g.db.query(Exhibit).filter_by(id=id).first()

    if not exhibit and not graceful:
        abort(404)

    return exhibit

def get_exhibits_by_ids(ids):

    id_list = []
    for i in ids:
        if isinstance(i, str):
            id_list.append(base36decode(i))
        else:
            id_list.append(i)

    exhibits = g.db.query(Exhibit).filter(Exhibit.id.in_(id_list)).order_by(Exhibit.id.desc()).all()
    return exhibits


def get_agency_by_id(id, graceful=False):

    if isinstance(id, str):
        id=base36decode(id)

    agency = g.db.query(Agency).filter_by(id=id).first()

    if not agency and not graceful:
        abort(404)

    return agency

def get_agency_by_domain(domain):

    # parse domain into all possible subdomains
    parts = domain.split(".")
    domain_list = set([])
    for i in range(len(parts)):
        new_domain = parts[i]
        for j in range(i + 1, len(parts)):
            new_domain += "." + parts[j]

        domain_list.add(new_domain)

    domain_list = tuple(list(domain_list))

    agencies = [x for x in g.db.query(Agency).filter(Agency.domain.in_(domain_list)).all()]

    if not agencies:
        return None

    # return the most specific agency - the one with the longest domain
    # property
    agencies = sorted(agencies, key=lambda x: len(x.domain), reverse=True)

    return agencies[0]

def get_bad_domain(domain):

    # parse domain into all possible subdomains
    parts = domain.split(".")
    domain_list = set([])
    for i in range(len(parts)):
        new_domain = parts[i]
        for j in range(i + 1, len(parts)):
            new_domain += "." + parts[j]

        domain_list.add(new_domain)

    domain_list = tuple(list(domain_list))

    domains = [x for x in g.db.query(BadDomain).filter(BadDomain.domain.in_(domain_list)).all()]

    if not domains:
        return None

    # return the most specific domain - the one with the longest domain
    # property
    domains = sorted(domains, key=lambda x: len(x.domain), reverse=True)

    return domains[0]

def get_lockershare_by_agency(victim, agency):

    if isinstance(agency, int):
        a_id = agency
    elif isinstance(agency, str):
        a_id = base36decode(agency)
    else:
        a_id = agency.id

    lockershare=g.db.query(LockerShare).filter_by(victim_id=victim.id, agency_id=a_id).first()

    return lockershare

def get_lockershare_by_leo(victim, leo):

    lockershare=g.db.query(LockerShare).filter_by(victim_id=victim.id, agency_id=leo.agency_id).first()

    return lockershare

def get_lockershare_by_exhibit_and_leo(exhibit, leo):

    lockershare=g.db.query(LockerShare).filter_by(victim_id=exhibit.author_id, agency_id=leo.agency_id).first()

    return lockershare

def get_blog_by_id(id):

    if isinstance(id, str):
        id=base36decode(id)

    blog = g.db.query(BlogPost).filter_by(id=id).first()

    if not blog:
        abort(404)

    return blog