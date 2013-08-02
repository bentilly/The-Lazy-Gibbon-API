import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb

from tlgDatastore import *
import email_service
import token_service


""" GET """
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
    
    
#TODO: switch this to a Token
def getUserByResetToken(resetToken):
    users = TLGUser.query(TLGUser.resetToken == resetToken).fetch(1)
    if users:
        for user in users:
            return user
    
    return None

""" CREATE """
def createUser(email, password, name):
    tlguser = TLGUser(id=email)
    tlguser.name = name
    tlguser.email = email;
    tlguser.password = password
    tlguser.put()
    
    return tlguser

def addUser(email, password, name, host_url):
    if getUserByEmail(email) != None:
        return
    
    tlguser = createUser(email, password, name)
    confToken = token_service.createEmailConfirmToken(tlguser)
    email_service.sendEmailConfirmation(tlguser, confToken, host_url)
        
    
    return tlguser


""" DELETE """