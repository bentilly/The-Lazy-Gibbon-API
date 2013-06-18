import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb

from tlgDatastore import *


'''class USERService(object):
    def __init__(self):
        return'''

'''----- USER -----'''

'''.....ADD.....'''
def addUser(email, password, name):
    if getUserByEmail(email) != None:
        return

    user = TLGUser()
    user.name = name
    user.email = email;
    user.password = password
    user.put()
    return user


'''.....GET.....'''
def getUserByEmail(email):
    users = TLGUser.query(TLGUser.email == email).fetch(1)
    if users:
        for user in users:
            return user

    return None

def getUserByEmailAndPassword(email, password):
    users = TLGUser.query(ndb.AND(TLGUser.email == email, TLGUser.password == password)).fetch(1)
    if users:
        for user in users:
            return user
    
    return None
    
    
    
def getUserByResetToken(resetToken):
    users = TLGUser.query(TLGUser.resetToken == resetToken).fetch(1)
    if users:
        for user in users:
            return user
    
    return None