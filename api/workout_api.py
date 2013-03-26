import webapp2
import json

import services.token_service
import services.workout_service

class TLG_WORKOUT(object):
    def __init__(self):
        return
    
    def addWorkout(self, jsonObj):
        #Authentication: Valid TOKEN
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            workout = services.workout_service.addWorkout(tlguser, jsonObj['date'], jsonObj['duration'], jsonObj['comment'], jsonObj['activity'])
            if workout:
                return '{"status":"success", "message":"workout created"}'
            else:
                return '{"status":"error", "message":"could not create workout"}'
            
        else:
            return '{"status":"error", "message":"invalid token"}'