import time
import secrets

from evidencelocker.decorators.lazy import lazy
from evidencelocker.helpers.b36 import *
from evidencelocker.helpers.hashes import *

from flask import *

class b36ids():

    @property
    def b36id(self):
        return base36encode(self.id)
    

class time_mixin():

    @property
    @lazy
    def created_string(self):
        return time.strftime("%d %B %Y at %H:%M:%S", time.gmtime(self.created_utc))

    @property
    @lazy
    def created_iso(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(self.created_utc))

    @property
    def age(self):
        return int(time.time()) - self.created_utc

class user_mixin():

    @property
    def is_banned(self):
        return bool(self.banned_utc)

    @property
    def csrf_token(self):

        if "session_id" not in session:
            session["session_id"]=secrets.token_hex(16)

        msg = f"{session['session_id']}+{self.type_id}+{self.login_nonce}"

        return generate_hash(msg)

    def validate_csrf_token(self, token):
        return validate_hash(f"{session['session_id']}+{self.type_id}+{self.login_nonce}", token)


    @property
    def otp_secret_reset_code(self):

        return compute_otp_recovery_code(self, self.otp_secret)

class json_mixin():

    @property
    def json(self):
        data=self.__dict__

        print(data)

        return data
    
    @property
    def jsonlink(self):
        return f"{self.permalink}.json"
    