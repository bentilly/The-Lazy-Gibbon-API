from google.appengine.ext import ndb
from tlgDatastore import *
import logging

import utils

def addActivity(name, tlguser, group, colour):
    activity = Activity()
    activity.name = name
    if tlguser:
        activity.tlguser = tlguser.key
    elif group:
        activity.group = group.key
        
    if colour:
        activity.colour = colour #TODO: validate
    else:
        activity.colour = utils.createRandomColour()
        
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
    


def updateActivity(keyString, name, colour):
    activity = getActivityByKEY(keyString)
    if activity:
        activity.name = name
        activity.colour = colour
        activity.put()
        
        return activity
    
    return
    
    
    
    
    
def getActivityByKEY(keyString):
    try:
        activityKey = ndb.Key(urlsafe=keyString)
        activity = activityKey.get()
        if activity:
            return activity
    except:
        return
    
    return