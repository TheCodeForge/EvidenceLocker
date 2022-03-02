from flask import *

from evidencelocker.helpers.loaders import *

def logged_in_victim(f):

    def wrapper(*args, **kwargs):
    
        if session.get("utype") != "v":
            abort(401)
            
        user = get_victim_by_id(session.get("uid"))
            
        return f(user, *args, **kwargs)
        
def logged_in_police(f):

    def wrapper(*args, **kwargs):
    
        if session.get("utype") != "p":
            abort(401)
            
        user = get_police_by_id(session.get("uid"))
            
        return f(user, *args, **kwargs)
