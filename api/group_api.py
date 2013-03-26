import webapp2
import json
import logging

from google.appengine.api import users

import services

#import services.token_service
#import services.group_service


class TLG_GROUP(object):
    def __init__(self):
        return
    
    def addGroup(self, jsonObj):
        #Authentication: Valid TOKEN
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.addGroup(jsonObj['name'], tlguser)
            if group:
                return '{"status":"success Group made"}'
            else:
                return '{"error":"group name already exists or some other error"}'
        else:
            return '{"error":"invalid token"}'


    def addInvite(self, jsonObj):
        #Authentication: Valid TOKEN, Valid GROUP ID, TOKEN.TLGUSER is ADMIN of GROUP
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.getGroupByID(jsonObj['group'])
            if group:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(group, tlguser)
                if groupAdmin:
                    #Authenticated
                    invite = services.group_service.addInvite(tlguser, group, jsonObj['email'], jsonObj['admin'])
                    if invite:
                        return '{"status":"success"}'
                    else:
                        return '{"status":"error", "message":"Could not create invite. Possible bad email"}'
                else:
                    return '{"status":"error", "message":"user not admin of group"}'
            else:
                return '{"status":"error", "message":"invalid group"}'
        else:
            return '{"status":"error", "message":"invalid token"}'
        
        
    def addMember(self, jsonObj):
        #Authentication: SYSADMIN ONLY
        user = users.get_current_user()
        if users.is_current_user_admin():
            member = services.group_service.addMember(jsonObj['email'], jsonObj['groupKey'])
            if member:
                return '{"status":"success", "message":"Group Member created"}'
            else:
                return '{"status":"error", "message":"failed to create member"}'
            
            
        else:
            url = users.create_login_url()
            return '{"status":"error", "message":"you need to be a system admin to do this"}'
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                