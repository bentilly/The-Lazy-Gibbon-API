import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb

from tlgDatastore import *

import utils
import tlguser_service


'''class GROUPService(object):
    def __init__(self):
        return'''
    
'''----- GROUP -----'''

'''.....ADD.....'''
def addGroup(name, tlguser):
    slug = utils.slugify(name)
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
    invite = Group_Invite()
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
    tlguser = tlguser_service.getUserByEmail(email)
    if group:
        if tlguser:
            member = Group_Member()
            member.tlguser = tlguser.key
            member.group = group.key
            member.put()
            logging.info(member)
            return member
        
    else:
        return

def addMemberFromObjects(tlguser, group):
    member = Group_Member()
    member.tlguser = tlguser.key
    member.group = group.key
    member.put()
    return member
    
    
'''.....GET.....'''
def getGroupByID(slug):
    group = Group.get_by_id(slug)
    if group:
        return group
    
    return None

def getGroupByKEY(keyString):
    try:
        groupKey = ndb.Key(urlsafe=keyString)
        group = groupKey.get()
        if group:
            return group
    except:
        return
    
    return

#Authentication
def getGroupAdminByGroupAndAdmin(group, tlguser):
    groupAdmin = Group_Admin.query(ndb.AND(Group_Admin.group == group.key, Group_Admin.tlguser == tlguser.key)).fetch(1)
    if groupAdmin:
        return groupAdmin
    
    return None

#Authentication
def getGroupMemberByGroupAndUser(group, tlguser):
    groupMember = Group_Member.query(ndb.AND(Group_Member.group == group.key, Group_Member.tlguser == tlguser.key)).fetch(1)
    if groupMember:
        return groupMember
    
    return None
    


def getGroupMembersFromUser(tlguser):
    groupMembers = Group_Member.query(Group_Member.tlguser == tlguser.key).fetch(50) #TODO: limit of 50 appropriate? Cursor?
    if len(groupMembers) > 0:
        groups = []
        for groupMember in groupMembers:
            groups.append( groupMember.group.get() )
            
        return groups
    
    return None



def getGroupAdminsFromUser(tlguser):
    groupAdmins = Group_Admin.query(Group_Admin.tlguser == tlguser.key).fetch(50)
    #TODO: limit of 50 appropriate? Cursor?
    if len(groupAdmins) > 0:
        groups = []
        for groupAdmin in groupAdmins:
            groups.append( groupAdmin.group.get() )
            
        return groups
    
    return None

def getMembers(group):
    groupMembers = Group_Member.query(Group_Member.group == group.key).fetch(100) #TODO: remove limit?
    return groupMembers
    
    
def getActivities(group):
    groupActivities = Activity.query(Activity.group == group.key).fetch(100) #TODO: remove limit?
    return groupActivities    
    
    
def getInvite(keyString):
    logging.info('getting invite')
    try:
        inviteKey = ndb.Key(urlsafe=keyString)
        invite = inviteKey.get()
        if invite:
            return invite
    except:
        return
    
    return
    
    
    
    
    
    
    
    