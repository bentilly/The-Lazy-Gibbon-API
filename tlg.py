import webapp2
import json
import logging


from api import token_api
from api import tlguser_api
from api import group_api
from api import activity_api
from api import workout_api

from services import token_service

TLG_TOKEN = token_api.TLG_TOKEN()
TLG_USER = tlguser_api.TLG_USER()
TLG_GROUP = group_api.TLG_GROUP()
TLG_ACTIVITY = activity_api.TLG_ACTIVITY()
TLG_WORKOUT = workout_api.TLG_WORKOUT()


class HomePage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/web/index.html")

class AppPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/app/index.html")


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
        
        try:
            if jsonObj['operation'] == 'token.createToken' or jsonObj['operation'] == 'user.signup':
                logString = jsonObj['email']
            else:
                tlguser = token_service.getUserFromToken(jsonObj['token'])
                logString = tlguser.name + " : " + tlguser.email
            
            logString += " : "
            logString += jsonObj['operation']
            logging.info(logString)
        except:
            logging.info('no "operation" supplied')
        
        
        '''----- TOKEN -----'''
        #same as login
        if jsonObj['operation'] == 'token.createToken':
            self.response.out.write(TLG_TOKEN.createToken(jsonObj))
            
            return
        
        '''----- USER -----'''
        if jsonObj['operation'] == 'user.signup':
            #get the host URL for creating full links (eg in emails)
            host_url = self.request.host_url
            self.response.out.write(TLG_USER.signup(jsonObj, host_url))
            return
        
        if jsonObj['operation'] == 'user.resetPassword':
            #get the host URL for creating full links (eg in emails)
            host_url = self.request.host_url
            self.response.out.write(TLG_USER.resetPassword(jsonObj, host_url))
            return
        
        if jsonObj['operation'] == 'user.getGroups':
            self.response.write(TLG_USER.getGroups(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getAdminGroups':
            self.response.write(TLG_USER.getAdminGroups(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getAllMyGroups':
            self.response.write(TLG_USER.getAllMyGroups(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getActivities':
            self.response.write(TLG_USER.getActivites(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getWorkouts':
            self.response.write(TLG_USER.getWorkouts(jsonObj))
            return
        
        if jsonObj['operation'] == 'user.getAllWorkouts':
            self.response.write(TLG_USER.getAllWorkouts(jsonObj))
            return
        
        #Returns the Google Login page URL
        if jsonObj['operation'] == 'user.getGoogleLoginPage':
            self.response.write(TLG_USER.getGoogleLoginPage())
            return
        
        '''----- GROUP -----'''
        if jsonObj['operation'] == 'group.addGroup':
            self.response.out.write(TLG_GROUP.addGroup(jsonObj))
            return
        
        if jsonObj['operation'] == 'group.editGroup':
            self.response.out.write(TLG_GROUP.editGroup(jsonObj))
            return

        if jsonObj['operation'] == 'group.getMemberWorkouts':
            self.response.out.write(TLG_GROUP.getMemberWorkouts(jsonObj))
            return
        
        if jsonObj['operation'] == 'group.getGroupInvites':
            self.response.out.write(TLG_GROUP.getGroupInvites(jsonObj))
            return
        
        if jsonObj['operation'] == 'group.addInvite':
            #get the host URL for creating full links (eg in emails)
            host_url = self.request.host_url
            self.response.out.write(TLG_GROUP.addInvite(jsonObj, host_url))
            return
        
        if jsonObj['operation'] == 'group.deleteInvite':
            self.response.out.write(TLG_GROUP.deleteInvite(jsonObj))
            return
        
        #SYSADMIN ONLY
        if jsonObj['operation'] == 'group.addMember':
            self.response.out.write(TLG_GROUP.addMember(jsonObj))
            return
        
        
        '''----- ACTIVITY -----'''
        if jsonObj['operation'] == 'activity.addActivity':
            self.response.out.write(TLG_ACTIVITY.addActivity(jsonObj))
            return
        
        if jsonObj['operation'] == 'activity.updateActivity':
            self.response.out.write(TLG_ACTIVITY.updateActivity(jsonObj))
            return
        
        '''----- WORKOUT -----'''
        if jsonObj['operation'] == 'workout.addWorkout':
            self.response.out.write(TLG_WORKOUT.addWorkout(jsonObj))
            return
        
        if jsonObj['operation'] == 'workout.updateWorkout':
            self.response.out.write(TLG_WORKOUT.updateWorkout(jsonObj))
            return
        
        if jsonObj['operation'] == 'workout.deleteWorkout':
            self.response.out.write(TLG_WORKOUT.deleteWorkout(jsonObj))
            return
        
        self.response.write('{"status":"error", "message":"Unknown Request"}')
        
app = webapp2.WSGIApplication([
								('/', HomePage),
                                ('/app', AppPage),
								('/api', APIHandler) 
								
								], debug=True)