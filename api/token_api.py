import webapp2
import json
import logging
import hashlib

from google.appengine.api import users

import services.token_service
import services.tlguser_service

#import services.token_service 

class TLG_TOKEN(object):
	def __init__(self):
		return
	
	def createToken(self, jsonObj):
		#Admin: login as user
		if users.is_current_user_admin():
			p = hashlib.md5()
			p.update('admin')
			if jsonObj['password'] == p.hexdigest():
				tlguser = services.tlguser_service.getUserByEmail(jsonObj['email'])
				if tlguser:
					token = services.token_service.addToken(tlguser, 'login')
					logging.info("Admin loggin in as: "+ tlguser.name+" - "+tlguser.email)
					
			else:
				#Authenticate as normal user: email, password
				token = services.token_service.createLoginToken(jsonObj['email'], jsonObj['password'])
				
		else:
			#Authentication: email, password
			token = services.token_service.createLoginToken(jsonObj['email'], jsonObj['password'])
		
		if token:
			user = token.tlguser.get()
			returnObj = {}
			returnObj['status'] = 'success'
			returnObj['token'] = str(token.key.urlsafe())
			returnObj['name'] = user.name;
			returnString = json.dumps(returnObj)
			return returnString
		else:
			return '{"status":"error", "message":"email and/or password dont match a user"}'