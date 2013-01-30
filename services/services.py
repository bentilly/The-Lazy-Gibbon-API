import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb
from tlgDatastore import *

class TLGService(object):
    def __init__(self):
        return

    '''----- TOKEN -----'''
    def createToken(self, email, password):
        user = self.getUserByEmailAndPassword(email, password)
        if user == None:
            return
        
        else:
            #delete all tokens for this person (limits user to one login at a time)
            self.clearAllUserTokens(user)
            #create new one
            token = self.addToken(user)
            return token
            
            
    def clearAllUserTokens(self, user):
        tokens = Token.query(Token.tlgUser == user.key).fetch()
        for token in tokens:
            token.key.delete()
            
        return
    
    
    def addToken(self, user):
        token = Token()
        token.tlgUser = user.key;
        token.put()
        
        return token
    
    def getUserFromToken(self, tokenString):
        tokenKey = ndb.Key(urlsafe=tokenString)
        token = tokenKey.get()
        userKey = token.tlgUser
        user = userKey.get()
        
        return user
        #TODO: error handling - bad token

    '''----- USER -----'''
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
    
    def getUserByEmailAndPassword(self, email, password):
        users = TLGUser.query(ndb.AND(TLGUser.email == email, TLGUser.password == password)).fetch(1)
        if users:
            for user in users:
                return user
        
        return None
    
    
    '''----- GROUP -----'''
    def addGroup(self, name, user):
        #TODO:Lowercase and URL friendly-ify the slugs
        slug = re.sub(r'\s', '', name)
        #check for existing group with this slug
        if self.getGroupByID(slug) != None:
            return
        
        else:
            group = TLGGroup(id=slug)
            group.name = name
            group.slug = slug
            group.put()
            
            #TODO: Add user as group admin
            return group
    
    def getGroupByID(self, slug):
        group = TLGGroup.get_by_id(slug)
        if group:
            return group
        
        return None
    
    
    
    
    
    