import webapp2


from google.appengine.ext import ndb

import os
import urllib
import jinja2
import hashlib
import logging

from services import tlguser_service
from services import token_service


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class Confirm(webapp2.RequestHandler):
    def get(self):
        token = token_service.getTokenFromKey(self.request.get('token'))
        if token:
            tlguser = token.tlguser.get()
            tlguser.emailConfirmed = True
            tlguser.put()
            token.key.delete()
            
            template_values = {'user':tlguser, 'host_url':self.request.host_url}
            template = JINJA_ENVIRONMENT.get_template('emailConfirm.html')
            self.response.write(template.render(template_values))
            
            
        else:
            logging.debug("no token")



app = webapp2.WSGIApplication([
                                ('/signup/confirmEmail', Confirm)
                                
                                ], debug=True)
