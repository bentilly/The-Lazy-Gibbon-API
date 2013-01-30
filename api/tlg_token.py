import webapp2
import json
import logging
from services import services

TLGService = services.TLGService()


class TLG_TOKEN(object):
	def __init__(self):
		return
	
	def createToken(self, jsonObj):
		#Authentication: email, password
		token = TLGService.createToken(jsonObj['email'], jsonObj['password'])
		
		if token:
			returnObj = {}
			returnObj['status'] = 'success'
			returnObj['token'] = str(token.key.urlsafe())
			returnString = json.dumps(returnObj)
			return returnString
		else:
			return '{"error":"email and/or password dont match a user"}'