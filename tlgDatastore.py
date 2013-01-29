from google.appengine.ext import ndb

class TLGUser(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)