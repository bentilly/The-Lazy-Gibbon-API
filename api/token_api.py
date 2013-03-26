import webapp2
import json
import logging

import services.token_service

#import services.token_service 

class TLG_TOKEN(object):
	def __init__(self):
		return
	
	def createToken(self, jsonObj):
		#Authentication: email, password
		token = services.token_service.createToken(jsonObj['email'], jsonObj['password'])
		
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