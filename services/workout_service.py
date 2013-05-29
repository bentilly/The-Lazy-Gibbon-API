import logging
import copy
from google.appengine.ext import ndb
import datetime

import utils

from tlgDatastore import *

import activity_service


def addWorkout(tlguser, date_string, duration_string, comment, activities, newActivity):
    #Validate
    duration = int(duration_string) #minutes
    if duration > 0:
        workout = Workout() #no id - to many of these. refer to them by url_safe
        workout.tlguser = tlguser.key
        dateList = date_string.split('-') #2013-3-23
        workout.date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        workout.duration = duration #minutes
        workout.comment = comment
        
        
        #Activities
        workoutActivities = []
        
        for a in activities:
            try:
                activityKey = ndb.Key(urlsafe=a)
                workoutActivities.append(activityKey)
            except:
                #do nothing
                a=0
            
        if newActivity:
            workoutActivities.append(newActivity.key)
        
        workout.activities = workoutActivities;

        workout.put()
        
        return workout
    
    return

def updateWorkout(workout, date_string, duration_string, comment, activities, newActivity):
    #Validate
    duration = int(duration_string) #minutes
    if duration > 0:
        dateList = date_string.split('-') #2013-3-23
        workout.date = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        workout.duration = duration #minutes
        workout.comment = comment
        
        #Activities
        workoutActivities = []
        
        for a in activities:
            try:
                activityKey = ndb.Key(urlsafe=a)
                workoutActivities.append(activityKey)
            except:
                #do nothing
                a=0
            
        if newActivity:
            workoutActivities.append(newActivity.key)
        
        workout.activities = workoutActivities;
            
        workout.put()
        
        return workout
    
    return


    
def getWorkoutsByUserAndDateRange(tlguser, startDate, endDate):
    workouts = Workout.query(Workout.tlguser == tlguser.key, Workout.date >= startDate, Workout.date <= endDate).fetch(1000) #TODO check limit of 1000. Is this OK?
    return workouts

def getWorkoutsByUserAndActivity(tlguserkey, activitykey):
    workouts = Workout.query(Workout.tlguser == tlguserkey, Workout.activities == activitykey).order(Workout.date).fetch(1000) #TODO check limit of 1000. Is this OK?
    return workouts

def getWorkoutSummariesByUserAndActivity(tlguserkey, activitykey):
    workouts = getWorkoutsByUserAndActivity(tlguserkey, activitykey)
    #group workouts by day and sum duration. Assumes ordered by date
    #setup: make first daySummary
    if workouts:
        workoutSummaries = []
        firstWorkout = workouts[0]
        currentDaySummary = {
                             'date':firstWorkout.date.strftime('%Y-%m-%d'),
                             'duration':0
                             }
        #create summaries
        for workout in workouts:
            if workout.date.strftime('%Y-%m-%d') == currentDaySummary['date']:
                currentDaySummary['duration'] = currentDaySummary['duration'] + workout.duration
            else:
                workoutSummaries.append(copy.deepcopy(currentDaySummary))
                currentDaySummary = {
                                     'date':workout.date.strftime('%Y-%m-%d'),
                                     'duration':workout.duration
                                     }
            
        workoutSummaries.append(copy.deepcopy(currentDaySummary)) #add the last one

        return workoutSummaries
    
    return None


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
    