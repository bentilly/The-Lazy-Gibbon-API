from google.appengine.ext import ndb

#TOKEN
class Token(ndb.Model):
    tlguser = ndb.KeyProperty(kind="TLGUser")
    created = ndb.DateTimeProperty(auto_now_add=True)
    #types of tokens: login, emailConfirm, (TODO:passwordReset)
    type = ndb.StringProperty(default='login')


#USER
class TLGUser(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    emailConfirmed = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    #for resetting lost passwords
    resetToken = ndb.StringProperty()
    resetCreated = ndb.DateProperty();
    
#GROUP
class Group(ndb.Model):
    name = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    
class Group_Member(ndb.Model):
    group = ndb.KeyProperty(kind="Group")
    tlguser = ndb.KeyProperty(kind="TLGUser")
    active = ndb.BooleanProperty(default=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    
class Group_Admin(ndb.Model):
    group = ndb.KeyProperty(kind="Group")
    tlguser = ndb.KeyProperty(kind="TLGUser")
    created = ndb.DateTimeProperty(auto_now_add=True)
    
class Group_Invite(ndb.Model):
    email = ndb.StringProperty()
    group = ndb.KeyProperty(kind="Group")
    invited_by = ndb.KeyProperty(kind="TLGUser")
    admin_invite = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    
#ACTIVITIES
class Activity(ndb.Model):
    name = ndb.StringProperty()
    tlguser = ndb.KeyProperty(kind="TLGUser")
    group = ndb.KeyProperty(kind="Group")
    colour = ndb.StringProperty()
#WORKOUT
class Workout(ndb.Model):
    tlguser = ndb.KeyProperty(kind="TLGUser")
    date = ndb.DateProperty()
    duration = ndb.IntegerProperty() #minutes
    comment = ndb.StringProperty()
    activities = ndb.KeyProperty(kind="Activity", repeated=True)#list of all activities associated with this workout. Doubles up on Workout_Activity but is easy to query
    
#class Workout_Activity(ndb.Model):
#    workout = ndb.KeyProperty(kind="Workout")
#    activity = ndb.KeyProperty(kind="Activity")
    
    