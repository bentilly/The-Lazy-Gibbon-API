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
                returnObj = {}
                returnObj['status'] = 'success'
                returnObj['key'] = group.key.urlsafe()
                s = json.dumps(returnObj)
                return s
            else:
                return '{"error":"no group created"}'
        else:
            return '{"status":"error", "message":"invalid token"}'
        
    def editGroup(self, jsonObj):
        #Authentication: Valid TOKEN
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.getGroupByKEY(jsonObj['key'])
            if group:
                services.group_service.editGroup(group, jsonObj['name'])
                return '{"status":"success"}'
            else:
                return '{"status":"error", "message":"could not find group"}'
        else:
            return '{"status":"error", "message":"invalid token"}'


    def addInvite(self, jsonObj, host_url):
        #Authentication: Valid TOKEN, Valid GROUP ID, TOKEN.TLGUSER is ADMIN of GROUP
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.getGroupByKEY(jsonObj['group'])
            if group:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(group, tlguser)
                if groupAdmin:
                    #Authenticated
                    try:
                        admin = jsonObj['admin']
                    except:
                        admin = None;
                    
                    invite = services.group_service.addInvite(tlguser, group, jsonObj['email'], admin)
                    if invite:
                        services.email_service.sendGroupInviteEmail(invite, host_url)
                        returnObj = {}
                        returnObj['status'] = 'success'
                        returnObj['key'] = invite.key.urlsafe()
                        s = json.dumps(returnObj)
            
                        return s

                    else:
                        return '{"status":"error", "message":"Could not create invite. Possible bad email"}'
                else:
                    return '{"status":"error", "message":"user not admin of group"}'
            else:
                return '{"status":"error", "message":"invalid group"}'
        else:
            return '{"status":"error", "message":"invalid token"}'
        
        
    def deleteInvite(self, jsonObj):
        #Authentication: Valid TOKEN, Valid GROUP_INVITE. TLGUSER is ADMIN of GROUP_INVITE.GROUP
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            # invite = services.group_service.getInviteByKey(jsonObj['key'])
            invite = services.utils.getEntityByKeystring(jsonObj['key'], 'Group_Invite')
            if invite:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(invite.group.get(), tlguser)
                if groupAdmin:
                    #Authenticated
                    if services.utils.deleteEntityByKey(invite.key, 'Group_Invite'):
                        return '{"status":"success", "message":"Invite deleted"}'
                    else:
                        return '{"status":"error", "message":"invite not deleted"}'
                else:
                    return '{"status":"error", "message":"not allowed to delete invite"}'
            else:
                return '{"status":"error", "message":"invalid invite"}'
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
                
                
    def getMemberWorkouts(self, jsonObj):
        #Authentication: Valid TOKEN, Valid GROUP. USER is MEMBER or ADMIN of group
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.getGroupByKEY(jsonObj['group'])
            if group:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(group, tlguser)
                groupMember = services.group_service.getGroupMemberByGroupAndUser(group, tlguser)
                if groupAdmin or groupMember:
                    #Authenticated
                    #setup  
                    returnObj = {}
                    memberList = []
                    #get group members
                    groupMembers = services.group_service.getMembers(group)
                    #get group activities
                    groupActivities = services.group_service.getActivities(group)
                    
                    #build response
                    for member in groupMembers:
                        memberUser = member.tlguser.get()
                        #group activities
                        activitySummaries = []
                        for groupActivity in groupActivities:
                            #get workouts for this user and activity
                            workoutSummaries = services.workout_service.getWorkoutSummariesByUserAndActivity(member.tlguser, groupActivity.key)
                            #make activity summary object
                            if workoutSummaries:
                                activitySummary = {
                                                   'activity':groupActivity.key.urlsafe(),
                                                   'workoutSummaries':workoutSummaries
                                                   }
                                activitySummaries.append(activitySummary)
                        
                        memberData = {
                                       'name':memberUser.name,
                                       'email':memberUser.email,
                                       'activities':activitySummaries
                                       }
                        
                        if memberUser == tlguser:
                            memberData['currentUser'] = 'true'
                        
                        memberList.append(memberData)
                    
                    returnObj['status'] = 'success'
                    returnObj['members'] = memberList
                    s = json.dumps(returnObj)
            
                    return s
                    
                    
                else:
                    return '{"status":"error", "message":"user not admin of group"}'
            else:
                return '{"status":"error", "message":"invalid group"}'
        else:
            return '{"status":"error", "message":"invalid token"}'
                
                
    def getGroupInvites(self, jsonObj):
        #Authentication: Valid TOKEN, Valid GROUP. USER is ADMIN of group
        tlguser = services.token_service.getUserFromToken(jsonObj['token'])
        if tlguser:
            group = services.group_service.getGroupByKEY(jsonObj['group'])
            if group:
                groupAdmin = services.group_service.getGroupAdminByGroupAndAdmin(group, tlguser)
                if groupAdmin:
                    invites = services.group_service.getGroupInvites(group)
                    
                    returnObj = {}
                    invitesList = []
                    
                    for invite in invites:
                        invitesList.append({'email':invite.email, 'key':invite.key.urlsafe()})
                    
                    returnObj['status'] = 'success'
                    returnObj['invites'] = invitesList
                    s = json.dumps(returnObj)
                    return s
                
        else:
            return '{"status":"error", "message":"invalid token"}'
                
                
                
                
                