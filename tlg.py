import webapp2
import json
import logging

from api import tlg_user

TLG_USER = tlg_user.TLG_USER()



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to The LAzy Gibbon web service')


class APIHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('APIHandler')

    def post(self):
        self.data = self.request.get('data')
        jsonObj = json.loads(self.data)
        
        #USER
        if jsonObj['operation'] == 'user.signup':
            self.response.out.write(TLG_USER.signup(jsonObj))
            return
        
        self.response.write('{"status":"error", "message":"Unknown Request"}')
        
app = webapp2.WSGIApplication([
								('/', MainPage),
								('/api', APIHandler) 
								
								], debug=True)