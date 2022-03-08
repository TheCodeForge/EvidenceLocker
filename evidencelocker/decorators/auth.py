from flask import *

from evidencelocker.helpers.loaders import get_victim_by_id, get_admin_by_id, get_police_by_id

def logged_in_victim(f):

    def wrapper(*args, **kwargs):

        if not session.get("uid"):
            abort(401)
    
        if session.get("utype") != "v":
            abort(403)
            
        user = get_victim_by_id(session.get("uid"))

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")
            
        return f(user, *args, **kwargs)
    
    wrapper.__name__=f.__name__
    return wrapper
        
def logged_in_police(f):

    def wrapper(*args, **kwargs):

        if not session.get("uid"):
            abort(401)
    
        if session.get("utype") != "p":
            abort(403)
            
        user = get_police_by_id(session.get("uid"))

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")
            
        return f(user, *args, **kwargs)
    
    wrapper.__name__=f.__name__
    return wrapper

def logged_in_admin(f):

    def wrapper(*args, **kwargs):

        if not session.get("uid"):
            abort(401)

        if session.get("utype") != "a":
            abort(403)

        user=get_admin_by_id(session.get("uid"))

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")

        return f(user, *args, **kwargs)

    wrapper.__name__=f.__name__
    return wrapper

def logged_in_any(f):

    def wrapper(*args, **kwargs):

        if not session.get("uid"):
            abort(401)

        utype=session.get("utype")
        uid=session.get("uid")

        if utype=="v":
            user = get_victim_by_id(uid)
        elif utype=="p":
            user = get_police_by_id(uid)
        elif utype=="a":
            user = get_admin_by_id(uid)
        else:
            abort(401)

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")

        return f(user, *args, **kwargs)

    wrapper.__name__=f.__name__
    return wrapper

def logged_in_desired(f):

    def wrapper(*args, **kwargs):

        utype=session.get("utype")
        uid=session.get("uid")

        if utype=="v":
            user = get_victim_by_id(uid)
        elif utype=="p":
            user = get_police_by_id(uid)
        elif utype=="a":
            user = get_admin_by_id(uid)
        else:
            user=None

        if user and not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")

        return f(user, *args, **kwargs)

    wrapper.__name__=f.__name__
    return wrapper

def not_banned(f):
    
    def wrapper(*args, **kwargs):
        
        user=args[0]
        
        if user.is_banned:
            abort(403)

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")
        
        return f(*args, **kwargs)
    
    wrapper.__name__=f.__name__
    return wrapper


def validate_csrf_token(f):
    """Always use authentication wrapper above this one"""

    def wrapper(user, *args, **kwargs):

        if not request.path.startswith("/api/v1"):

            submitted_key = request.values.get("csrf_token", "none")

            if not submitted_key:
                abort(401)

            elif not user.validate_csrf_token(submitted_key):
                abort(401)

        return f(*args, v=v, **kwargs)

    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper