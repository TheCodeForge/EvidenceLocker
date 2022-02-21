import time

from evidencelocker.decorators.lazy import lazy

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