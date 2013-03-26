import webapp2
import json
import logging


from api import token_api
from api import tlguser_api
from api import group_api
from api import activity_api
from api import workout_api

TLG_TOKEN = token_api.TLG_TOKEN()
TLG_USER = tlguser_api.TLG_USER()
TLG_GROUP = group_api.TLG_GROUP()
TLG_ACTIVITY = activity_api.TLG_ACTIVITY()
TLG_WORKOUT = workout_api.TLG_WORKOUT()



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to The LAzy Gibbon web service')


class APIHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('APIHandler')
        
        
    '''
    ----- API LAYER -----
    Distributes the requests to the appropriate api handlers
    '''
    def post(self):
        self.data = self.request.get('data')
        jsonObj = json.loads(self.data)
        
        '''----- TOKEN -----'''
        #same as login
        if jsonObj['operation'] == 'token.createToken':
            self.response.out.write(TLG_TOKEN.createToken(jsonObj))
            return
        
        '''----- USER -----'''
        if jsonObj['operation'] == 'user.signup':
            self.response.out.write(TLG_USER.signup(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getGroups':
            self.response.write(TLG_USER.getGroups(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getAdminGroups':
            self.response.write(TLG_USER.getAdminGroups(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getActivities':
            self.response.write(TLG_USER.getActivites(jsonObj))
            return
        
        #Returns the Google Login page URL
        if jsonObj['operation'] == 'user.getGoogleLoginPage':
            self.response.write(TLG_USER.getGoogleLoginPage())
            return
        
        '''----- GROUP -----'''
        if jsonObj['operation'] == 'group.addGroup':
            self.response.out.write(TLG_GROUP.addGroup(jsonObj))
            return
        
        if jsonObj['operation'] == 'group.addInvite':
            self.response.out.write(TLG_GROUP.addInvite(jsonObj))
            return
        
        #SYSADMIN ONLY
        if jsonObj['operation'] == 'group.addMember':
            self.response.out.write(TLG_GROUP.addMember(jsonObj))
            return
        
        '''----- ACTIVITY -----'''
        if jsonObj['operation'] == 'activity.addActivity':
            self.response.out.write(TLG_ACTIVITY.addActivity(jsonObj))
            return
        
        '''----- WORKOUT -----'''
        if jsonObj['operation'] == 'workout.addWorkout':
            self.response.out.write(TLG_WORKOUT.addWorkout(jsonObj))
            return
        
        self.response.write('{"status":"error", "message":"Unknown Request"}')
        
app = webapp2.WSGIApplication([
								('/', MainPage),
								('/api', APIHandler) 
								
								], debug=True)