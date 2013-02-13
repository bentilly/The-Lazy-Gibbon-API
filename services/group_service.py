import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb

from tlgDatastore import *

import services.utils
import services.tlguser_service


'''class GROUPService(object):
    def __init__(self):
        return'''
    
'''----- GROUP -----'''

'''.....ADD.....'''
def addGroup(name, tlguser):
    slug = services.utils.slugify(name)
    #check for existing group with this slug
    if getGroupByID(slug) != None:
        return
    
    else:
        group = Group(id=slug)
        group.name = name
        group.put()
        
        groupAdmin = addGroupAdmin(group, tlguser)
        #TODO:catch a fail at Group or GroupAdmin and fail the whole process
        
        return group

def addGroupAdmin(group, tlguser):
    groupSlug = group.key.id()
    tlguserSlug = tlguser.key.id()
    groupAdminSlug = groupSlug + '~admin~' + tlguserSlug
    
    groupAdmin = Group_Admin(id = groupAdminSlug)
    groupAdmin.group = group.key
    groupAdmin.tlguser = tlguser.key
    groupAdmin.put()
    
    return groupAdmin

def addInvite(tlguser, group, email, admin):
    slug = group.key.id() + '~invite~' + email + '~by~' + tlguser.key.id()
    invite = Group_Invite(id = slug)
    
    invitedUser = services.tlguser_service.getUserByEmail(email)
    if invitedUser:
        invite.tlguser = invitedUser.key
    else:
        invite.email = email
        
    invite.group = group.key
    invite.invited_by = tlguser.key
    if admin == 'true':
        invite.admin_invite = True
    invite.put()
    
    return invite

def addMember(email, groupString):
    groupKey = ndb.Key(urlsafe=groupString)
    group = groupKey.get()
    tlguser = services.tlguser_service.getUserByEmail(email)
    if group:
        if tlguser:
            slug = group.key.id() + '~member~' + tlguser.key.id()
            member = Group_Member(id = slug)
            member.tlguser = tlguser.key
            member.group = group.key
            member.put()
            return member
        
    else:
        return
    
    
    
'''.....GET.....'''
def getGroupByID(slug):
    group = Group.get_by_id(slug)
    if group:
        return group
    
    return None


def getGroupAdminByGroupAndAdmin(group, tlguser):
    groupAdmin = Group_Admin.query(ndb.AND(Group_Admin.group == group.key, Group_Admin.tlguser == tlguser.key)).fetch(1)
    if groupAdmin:
        return groupAdmin
    
    return None
    


def getGroupMembersFromUser(tlguser):
    groupMembers = Group_Member.query(Group_Member.tlguser == tlguser.key).fetch(50) #TODO: limit of 50 appropriate? Cursor?
    if groupMembers:
        return groupMembers
    
    return None



def getGroupAdminsFromUser(tlguser):
    groupAdmins = Group_Admin.query(Group_Admin.tlguser == tlguser.key).fetch(50)
    #TODO: limit of 50 appropriate? Cursor?
    if groupAdmins:
        return groupAdmins
    
    return None


    