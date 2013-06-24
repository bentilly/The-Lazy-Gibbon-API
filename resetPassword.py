import webapp2


from google.appengine.ext import ndb

import os
import urllib
import jinja2
import hashlib
import logging

from services import tlguser_service


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class ResetPasswordPage(webapp2.RequestHandler):
    def get(self):
        logging.debug("go Reset Password Page")
        tlguser = tlguser_service.getUserByResetToken(self.request.get('resetToken'))
        if tlguser:
            logging.debug("found user")
            template_values = {'user':tlguser}
            template = JINJA_ENVIRONMENT.get_template('resetPassword.html')
            self.response.write(template.render(template_values))
        else:
            logging.debug("no user")
            

class ResetPasswordSubmit(webapp2.RequestHandler):
    def post(self):
        tlguser = tlguser_service.getUserByResetToken(self.request.get('resetToken'))
        if tlguser:
            if self.request.get('password') == self.request.get('confirm'):
                # reset the password
                p = hashlib.md5()
                p.update(self.request.get('password'))
                tlguser.password = p.hexdigest()
                # delete the reset
                tlguser.resetToken = None
                tlguser.resetCreated = None
                tlguser.put()
                #display thanks page
                template_values = {'user':tlguser, 'host_url':self.request.host_url}
                template = JINJA_ENVIRONMENT.get_template('resetPasswordConfirm.html')
                self.response.write(template.render(template_values))
                
            else:
                template_values = {'user':tlguser,
                                   'message': 'Please check your passwords match'
                                   }
                template = JINJA_ENVIRONMENT.get_template('resetPassword.html')
                self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
                                ('/reset/resetPasswordPage', ResetPasswordPage),
                                ('/reset/resetPasswordSubmit', ResetPasswordSubmit)
                                ], debug=True)
