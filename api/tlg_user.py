import webapp2

from services import services

TLGService = services.TLGService()

import tlgDatastore

class TLG_USER(object):
	def __init__(self):
		return
	
	
	def signup(self, jsonObj):
		#Authentication: NONE
		user = TLGService.addUser(jsonObj['email'], jsonObj['password'], jsonObj['name'])
		
		if user:
			return '{"status":"success"}'
		else:
			return '{"error":"User already exists"}'
		