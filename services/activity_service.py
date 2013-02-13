from google.appengine.ext import ndb
from tlgDatastore import *
import logging

import services.utils

def addActivity(name, tlguser, group):
    if tlguser:
        ownerslug = tlguser.key.id()
    elif group:
        ownerslug = group.key.id()
    nameslug = services.utils.slugify(name)
    slug = ownerslug + '~activity~' + nameslug
    
    activity = Activity(id = slug)
    activity.name = name
    if tlguser:
        activity.tlguser = tlguser.key
        ownerslug = tlguser.key.id()
    elif group:
        activity.group = group.key
        ownerslug = group.key.id()
        
    activity.put()
    
    return activity

def getActivities(owner):
    if owner.key.kind() == "TLGUser":
        activities = Activity.query(Activity.tlguser == owner.key).fetch(100) #TODO: is 100 enough? to slow?
        return activities
    elif owner.key.kind() == "Group":
        activities = Activity.query(Activity.group == owner.key).fetch(100) #TODO: is 100 enough? to slow?
        return activities
    else:
        return