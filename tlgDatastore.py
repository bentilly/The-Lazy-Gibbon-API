from google.appengine.ext import ndb

#TOKEN
class Token(ndb.Model):
    tlgUser = ndb.KeyProperty(kind="TLGUser")
    date = ndb.DateTimeProperty(auto_now=True)


#USER
class TLGUser(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    
#GROUP
class TLGGroup(ndb.Model):
    name = ndb.StringProperty()
    slug = ndb.StringProperty()
    #add other properties later, eg description