from flask import *

from evidencelocker.helpers.loaders import *

def logged_in_victim(f):

    def wrapper(*args, **kwargs):

        if not session.get("uid"):
            abort(401)
    
        if session.get("utype") != "v":
            abort(403)
            
        user = get_victim_by_id(session.get("uid"))

        if not user.otp_secret and request.path != "/set_otp" and not request.path.startswith("/otp_secret_qr/"):
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

        if not user.otp_secret and request.path != "/set_otp" and not request.path.startswith("/otp_secret_qr/"):
            return redirect("/set_otp")

        if not user.is_recently_verified and request.path !="/verify_email":
            return redirect("/verify_email")
            
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

        if not user.otp_secret and request.path != "/set_otp" and not request.path.startswith("/otp_secret_qr/"):
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

        if not user.otp_secret and request.path != "/set_otp" and not request.path.startswith("/otp_secret_qr/"):
            return redirect("/set_otp")

        if user.type_id.startswith('p') and not user.is_recently_verified and request.path != "/verify_email":
            return redirect("/verify_email")

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
            return render_template("banned.html", user=user), 403

        if not user.otp_secret and request.path != "/set_otp":
            return redirect("/set_otp")
        
        return f(*args, **kwargs)
    
    wrapper.__name__=f.__name__
    return wrapper


def validate_csrf_token(f):
    """Always use authentication wrapper above this one"""

    def wrapper(user, *args, **kwargs):

        submitted_key = request.values.get("csrf_token", "none")

        if not submitted_key:
            abort(401)

        elif not user.validate_csrf_token(submitted_key):
            abort(401)

        return f(user, *args, **kwargs)

    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper