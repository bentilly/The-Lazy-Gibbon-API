import logging
import re #stripping whitespace for slugs
import random
import string
from random import randrange
from google.appengine.ext import ndb

'''class UTILS(object):
    def __init__(self):
        return'''
    
def slugify(string):
    #TODO:Lowercase and URL friendly-ify the slugs
    slug = re.sub(r'\s', '', string)
    slug = slug.lower()
    return slug
    
def createRandomColour():
    return "%s" % "".join([hex(randrange(0, 255))[2:] for i in range(3)])

def createRandomString(length):
    sample = string.lowercase + string.digits
    return ''.join(random.choice(sample) for i in range(length))

#get an entitiy by url-safe key string. Checks its the 'kind' you wanted
def getEntityByKeystring(keyString, kind):
    try:
        key = ndb.Key(urlsafe=keyString)
        if key.kind() == kind:
            entity = key.get()
            if entity:
                return entity
    except:
        return
    
    return

#delete an entitiy by url-safe key string. Safety check - chek the 'kind' before deleting
def deleteEntityByKey(key, kind):
    try:
        if key.kind() == kind:
            key.delete()
            return True
    except:
        return
    
    return