import logging
from google.appengine.ext import ndb

from tlgDatastore import *

import tlguser_service

#from services import tlguser_service
#import services.tlguser_service

""" GET """
def getUserFromToken(tokenString):
    try:
        token = getTokenFromKey(tokenString)
        if token:
            userKey = token.tlguser
            user = userKey.get()
            return user
        else:
            return
    except:
        return
    
    
def getTokenFromKey(keyString):
    tokenKey = ndb.Key(urlsafe=keyString)
    token = tokenKey.get()
    if token:
        return token
    
    return None



""" CREATE """
def addToken(user, type):
    token = Token()
    token.tlguser = user.key;
    token.type = type;
    token.put()
    
    return token

def createLoginToken(email, password):
    tlguser = tlguser_service.getUserByEmailAndPassword(email, password)
    if tlguser == None:
        return
    
    else:
        #delete all tokens for this person (limits user to one login at a time)
        clearAllUserLoginTokens(tlguser)
        #create new one
        token = addToken(tlguser, 'login')
        return token
        

def createLoginTokenFromUser(tlguser):
    #delete all tokens for this person (limits user to one login at a time)
    clearAllUserLoginTokens(tlguser)
    #create new one
    token = addToken(tlguser, 'login')
    return token


def createEmailConfirmToken(tlguser):
    token = addToken(tlguser, 'emailConfirm')
    return token

    

""" DELETE """
def clearAllUserLoginTokens(user):
    tokens = Token.query(Token.tlguser == user.key, Token.type == 'login').fetch()
    for token in tokens:
        token.key.delete()
        
    return









