import webapp2
import json
import logging
from services import services


TLGService = services.TLGService()

class TLG_GROUP(object):
    def __init__(self):
        return
    
    def addGroup(self, jsonObj):
        #Authentication: Valid TOKEN
        user = TLGService.getUserFromToken(jsonObj['token'])
        if user:
            group = TLGService.addGroup(jsonObj['name'], user)
            if group:
                return '{"status":"success Group made"}'
            else:
                return '{"error":"group name already exists or some other error"}'
        else:
            return '{"error":"invalid token"}'