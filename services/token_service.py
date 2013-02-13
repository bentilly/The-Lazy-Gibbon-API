import logging
from google.appengine.ext import ndb

from tlgDatastore import *

import services.tlguser_service

'''class TOKENService(object):
    def __init__(self):
        return'''

'''----- TOKEN -----'''
def createToken(email, password):
    user = services.tlguser_service.getUserByEmailAndPassword(email, password)
    if user == None:
        return
    
    else:
        #delete all tokens for this person (limits user to one login at a time)
        clearAllUserTokens(user)
        #create new one
        token = addToken(user)
        return token
        
        
def clearAllUserTokens(user):
    tokens = Token.query(Token.tlguser == user.key).fetch()
    for token in tokens:
        token.key.delete()
        
    return


def addToken(user):
    token = Token()
    token.tlguser = user.key;
    token.put()
    
    return token

def getUserFromToken(tokenString):
    try:
        tokenKey = ndb.Key(urlsafe=tokenString)
        token = tokenKey.get()
        if token:
            userKey = token.tlguser
            user = userKey.get()
            return user
        else:
            return
    except:
        return