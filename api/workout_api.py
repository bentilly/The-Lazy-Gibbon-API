import webapp2
import json

import services.token_service
import services.workout_service
import services.activity_service

class TLG_WORKOUT(object):
    def __init__(self):
        return
    
    def addWorkout(self, jsonObj):
        #Authentication: Valid TOKEN
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            #check if there is an activity tag
            if jsonObj['activity']:
                activityKeyString = jsonObj['activity']
            else:
                activityKeyString = None
            
            #check if this is a new activity (personal activity only)
            if jsonObj['newActivity']:
                #make new activity
                newActivity = services.activity_service.addActivity(jsonObj['newActivity'], tlguser, None, None)
                activityKeyString = newActivity.key.urlsafe()
            else:
                newActivity = None
                
            workout = services.workout_service.addWorkout(tlguser, jsonObj['date'], jsonObj['duration'], jsonObj['comment'], activityKeyString)
            
            if workout:
                returnObj = {}
                returnObj['status'] = 'success'
                returnObj['key'] = workout.key.urlsafe();
                returnObj['message'] = 'workout created'
                
                if newActivity:
                    returnObj['activityName'] = newActivity.name
                    returnObj['activityKey'] = newActivity.key.urlsafe();
                    returnObj['activityColour'] = newActivity.colour;
                    
                s = json.dumps(returnObj)
                return s
            
            else:
                return '{"status":"error", "message":"could not create workout"}'
            
        else:
            return '{"status":"error", "message":"invalid token"}'
        
        
    def updateWorkout(self, jsonObj):
        #Authentication: Valid TOKEN
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            #get workout
            workout = services.workout_service.getWorkoutByKEY(jsonObj['key']);
            if workout:
                #check user is allowed to edit workout
                if workout.tlguser == tlguser.key:
                    #User and workout authenticated. Update workout and save
                    #check if there is an activity tag
                    if jsonObj['activity']:
                        activityKeyString = jsonObj['activity']
                    else:
                        activityKeyString = None
                    
                    #check if this is a new activity (personal activity only)
                    if jsonObj['newActivity']:
                        #make new activity
                        newActivity = services.activity_service.addActivity(jsonObj['newActivity'], tlguser, None, None)
                        activityKeyString = newActivity.key.urlsafe()
                    else:
                        newActivity = None
                    
                    #Update
                    workout = services.workout_service.updateWorkout(workout, jsonObj['date'], jsonObj['duration'], jsonObj['comment'], activityKeyString)
                    #TODO: error handling
                    
                    if workout:
                        returnObj = {}
                        returnObj['status'] = 'success'
                        returnObj['key'] = workout.key.urlsafe();
                        returnObj['message'] = 'workout updated'
                        
                        if newActivity:
                            returnObj['activityName'] = newActivity.name
                            returnObj['activityKey'] = newActivity.key.urlsafe();
                            returnObj['activityColour'] = newActivity.colour;
                            
                        s = json.dumps(returnObj)
                        return s
                    
                    else:
                        return '{"status":"error", "message":"could not update workout"}'
            
            
            return '{"status":"error", "message":"invalid user or workout"}'
        else:
            return '{"status":"error", "message":"invalid token"}'
        
        
        
        
        
        
        
        
        
        
        
        
        