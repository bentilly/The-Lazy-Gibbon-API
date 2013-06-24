import webapp2


from google.appengine.ext import ndb

import os
import urllib
import jinja2
import hashlib
import logging

from services import tlguser_service
from services import group_service


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


class InvitePage(webapp2.RequestHandler):
    def get(self):
        invite = group_service.getInvite(self.request.get('inviteKey'))
        if invite:
            tlguser = tlguser_service.getUserByEmail(invite.email)
            if tlguser:
                #make member
                group = invite.group.get()
                member = group_service.addMemberFromObjects(tlguser, group)
                #delete invite
                invite.key.delete()
                #confirmation page
                template_values = {'invite':invite, 'user':tlguser, 'host_url':self.request.host_url}
                template = JINJA_ENVIRONMENT.get_template('inviteConfirm.html')
                self.response.write(template.render(template_values))
            else:
                #signup page
                template_values = {'invite':invite}
                template = JINJA_ENVIRONMENT.get_template('inviteSignup.html')
                self.response.write(template.render(template_values))
            
            
        else:
            logging.debug("no invite")

class InviteSignup(webapp2.RequestHandler):
    def post(self):
        invite = group_service.getInvite(self.request.get('inviteKey'))
        if invite:
            if self.request.get('password') == self.request.get('confirm'):
                #make new user
                p = hashlib.md5()
                p.update(self.request.get('password'))
                tlguser = tlguser_service.addUser(invite.email, p.hexdigest(), self.request.get('name'), self.request.host_url)
                #make member
                group = invite.group.get()
                member = group_service.addMemberFromObjects(tlguser, group)
                #delete invite
                invite.key.delete()
                #confirmation page
                template_values = {'invite':invite, 'user':tlguser, 'host_url':self.request.host_url}
                template = JINJA_ENVIRONMENT.get_template('inviteConfirm.html')
                self.response.write(template.render(template_values))
                return
            else:
                template_values = {'invite':invite,
                                   'message': 'Please check your passwords match'
                                   }
                template = JINJA_ENVIRONMENT.get_template('inviteSignup.html')
                self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
                                ('/groupInvite/invitePage', InvitePage),
                                ('/groupInvite/inviteSignup', InviteSignup)
                                
                                ], debug=True)
