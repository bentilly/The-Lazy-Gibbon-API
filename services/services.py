import logging

from google.appengine.ext import ndb
from tlgDatastore import *

class TLGService(object):
    def __init__(self):
        return

#USERS
    #USERS
    def addUser(self, email, password, name):
        if self.getUserByEmail(email) != None:
            return

        user = TLGUser(id=email)
        user.name = name
        user.email = email;
        user.password = password
        user.put()
        return user

    def getUserByEmail(self, email):
        user = TLGUser.query(TLGUser.email == email).fetch(1)
        if user:
            return user
        
        return None