import webapp2
import json
import logging

from api import tlg_token
from api import tlg_user
from api import tlg_group

TLG_TOKEN = tlg_token.TLG_TOKEN()
TLG_USER = tlg_user.TLG_USER()
TLG_GROUP = tlg_group.TLG_GROUP()



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
        
        '''----- GROUP -----'''
        if jsonObj['operation'] == 'group.addGroup':
            self.response.out.write(TLG_GROUP.addGroup(jsonObj))
            return
        
        self.response.write('{"status":"error", "message":"Unknown Request"}')
        
app = webapp2.WSGIApplication([
								('/', MainPage),
								('/api', APIHandler) 
								
								], debug=True)