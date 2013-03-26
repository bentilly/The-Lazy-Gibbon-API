import logging
from google.appengine.ext import ndb
import datetime

import utils

from tlgDatastore import *


def addWorkout(tlguser, date_string, duration_string, comment, activity_urlsafe):
    #Validate
    duration = int(duration_string) #minutes
    if duration > 0:
        activityKey = ndb.Key(urlsafe=activity_urlsafe)
        activity = activityKey.get()
        if activity:
            workout = Workout() #no id - to many of these. refer to them by url_safe
            workout.tlguser = tlguser.key
            dateList = date_string.split('-') #2013-3-23
            workout.date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
            workout.duration = duration #minutes
            workout.comment = comment
            workout.put()
            
            #TODO: for each activity in list
            workoutActivity = Workout_Activity()
            workoutActivity.workout = workout.key
            workoutActivity.activity = activity.key
            workoutActivity.put()
            
            return workout
            
        
    return #TODO:  error handling - more info on what went wrong
    
    