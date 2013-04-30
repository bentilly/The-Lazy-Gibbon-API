import logging
from google.appengine.ext import ndb
import datetime

import utils

from tlgDatastore import *

import activity_service


def addWorkout(tlguser, date_string, duration_string, comment, activity_urlsafe):
    #Validate
    duration = int(duration_string) #minutes
    if duration > 0:
        workout = Workout() #no id - to many of these. refer to them by url_safe
        workout.tlguser = tlguser.key
        dateList = date_string.split('-') #2013-3-23
        workout.date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        workout.duration = duration #minutes
        workout.comment = comment
        
        
        #TODO: for each activity in list
        if activity_urlsafe:    
            activityKey = ndb.Key(urlsafe=activity_urlsafe)
            activity = activityKey.get()
        else:
            activity = None
        
        if activity:
            #workoutActivity = Workout_Activity()
            #workoutActivity.workout = workout.key
            #workoutActivity.activity = activity.key
            #workoutActivity.put()
            
            workout.activities = [activity.key]
            
            
        workout.put()
        
        return workout
            
        
    return #TODO:  error handling - more info on what went wrong

def updateWorkout(workout, date_string, duration_string, comment, activity_urlsafe):
    #Validate
    duration = int(duration_string) #minutes
    if duration > 0:
        dateList = date_string.split('-') #2013-3-23
        workout.date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        workout.duration = duration #minutes
        workout.comment = comment
        
        #TODO: for each activity in list
        if activity_urlsafe:
            activityKey = ndb.Key(urlsafe=activity_urlsafe)
            activity = activityKey.get()
        else:
            activity = None
        
        if activity:
            workout.activities = [activity.key]
            
        workout.put()
        
        return workout
    
    return #TODO:  error handling - more info on what went wrong


    
def getWorkoutsByUserAndDateRange(tlguser, startDate, endDate):
    workouts = Workout.query(Workout.tlguser == tlguser.key, Workout.date >= startDate, Workout.date <= endDate).fetch(1000) #TODO check limit of 1000. Is this OK?
    return workouts

def getAllWorkoutsByUser(tlguser):
    workouts = Workout.query(Workout.tlguser == tlguser.key).order(-Workout.date).fetch(1000) #TODO check limit of 1000. Is this OK?
    return workouts

def getWorkoutByKEY(keyString):
    try:
        workoutKey = ndb.Key(urlsafe=keyString)
        workout = workoutKey.get()
        if workout:
            return workout
        #TODO: check entity is actually a Workout
    except:
        return
    
    return
    