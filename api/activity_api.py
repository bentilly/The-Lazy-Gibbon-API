import webapp2
import json
import logging

import services.token_service
import services.group_service
import services.activity_service

class TLG_ACTIVITY(object):
    def __init__(self):
        return
    
    def addActivity(self, jsonObj):
        #Authentication: Valid TOKEN, If GROUP, Valid GROUP ID, TOKEN.TLGUSER is ADMIN of GROUP
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            #Authenticated as user. Create Activity
            try:
                group = services.group_service.getGroupByID(jsonObj['group'])
            except:
                group = None
                
            if group:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(group, tlguser)
                if groupAdmin:
                    #Authenticated as group admin
                    activity = services.activity_service.addActivity(jsonObj['name'], None, group)
                    return '{"status":"success", "message":"created group activity"}'
                else:
                    #not group admin
                    return '{"status":"error", "message":"not group admin"}'
            else:
                #no group
                activity = services.activity_service.addActivity(jsonObj['name'], tlguser, None)
                return '{"status":"success", "message":"created user activity"}'
                
        else:
            return '{"status":"error", "message":"bad token"}'