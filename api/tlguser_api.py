import webapp2
import json
import datetime
from google.appengine.api import users

import services.tlguser_service
import services.group_service
import services.activity_service

#import services.tlguser_service
#import services.token_service
#import services.activity_service

class TLG_USER(object):
	def __init__(self):
		return
	
	
	def signup(self, jsonObj):
		#Authentication: NONE
		tlguser = services.tlguser_service.addUser(jsonObj['email'], jsonObj['password'], jsonObj['name'])
		
		if tlguser:
			return '{"status":"success"}'
		else:
			return '{"error":"User already exists"}'
	


	def getGroups(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			groupMembers = services.group_service.getGroupMembersFromUser(tlguser)
			
			returnObj = {}
			groupList = []
			
			if groupMembers:
				for groupMember in groupMembers:
					group = groupMember.group.get()
					groupList.append({'name':group.name, 'key':group.key.urlsafe()})
			
			returnObj['status'] = 'success'
			returnObj['groups'] = groupList
			s = json.dumps(returnObj)
			return s
			
		else:
			return '{"status":"error", "message":"invalid token"}'
		
	
	
	def getAdminGroups(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			groupAdmins = services.group_service.getGroupAdminsFromUser(tlguser)
			
			returnObj = {}
			groupList = []
			
			if groupAdmins:
				for group in groupAdmins:
					groupList.append({'name':group.name, 'key':group.key.urlsafe()})
			
			returnObj['status'] = 'success'
			returnObj['adminGroups'] = groupList
			s = json.dumps(returnObj)
			return s
			
		else:
			return '{"status":"error", "message":"invalid token"}'
		
		
	def getAllMyGroups(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		if tlguser:
			#get groups I admin
			groupAdmins = services.group_service.getGroupAdminsFromUser(tlguser)
			#get groups I am a member of
			groupMembers = services.group_service.getGroupMembersFromUser(tlguser)
			
			returnObj = {}
			groupList = []
			
			if groupAdmins:
				for group in groupAdmins:
					groupObject = {'name':group.name, 'key':group.key.urlsafe(), 'admin':'true'}
					#check if member and admin
					if groupMembers:
						if group in groupMembers:
							groupObject['member'] = 'true'
					groupList.append(groupObject)
					
					
			if groupMembers:
				for group in groupMembers:
					#check for double ups
					if groupAdmins:
						if group not in groupAdmins:
							groupList.append({'name':group.name, 'key':group.key.urlsafe(), 'member':'true'})
							
					else:
						groupList.append({'name':group.name, 'key':group.key.urlsafe(), 'member':'true'})
			
			
			returnObj['status'] = 'success'
			returnObj['groups'] = groupList
			s = json.dumps(returnObj)
			
			return s
		
		else:
			return '{"status":"error", "message":"invalid token"}'
		
		
	def getActivites(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			#get my personal activities
			activities = services.activity_service.getActivities(tlguser)
			#get groups I admin
			groupAdmins = services.group_service.getGroupAdminsFromUser(tlguser)
			#get groups I am a member of
			groupMembers = services.group_service.getGroupMembersFromUser(tlguser)
			
			returnObj = {}
			myActivities = []
			
			#my activities
			if activities:
				for  activity in activities:
					myActivities.append({'name':activity.name, 'key':activity.key.urlsafe(), 'colour':activity.colour})
			
			#my groups activities
			groups = []
			if groupAdmins:
				for g in groupAdmins:
					group = {'key':g.key.urlsafe()}
					groupActivities = services.activity_service.getActivities(g)
					activities = []
					for activity in groupActivities:
						activities.append({'name':activity.name, 'key':activity.key.urlsafe(), 'colour':activity.colour})
					group['activities'] = activities
					groups.append(group)
				
			if groupMembers:
				for g in groupMembers:
					if groupAdmins:
						if g not in groupAdmins:
							group = {'key':g.key.urlsafe()}
							groupActivities = services.activity_service.getActivities(g)
							activities = []
							for activity in groupActivities:
								activities.append({'name':activity.name, 'key':activity.key.urlsafe(), 'colour':activity.colour})
							group['activities'] = activities
							groups.append(group)
					else:
						group = {'key':g.key.urlsafe()}
						groupActivities = services.activity_service.getActivities(g)
						activities = []
						for activity in groupActivities:
							activities.append({'name':activity.name, 'key':activity.key.urlsafe(), 'colour':activity.colour})
						group['activities'] = activities
						groups.append(group)
			
			
			returnObj['status'] = 'success'
			returnObj['activities'] = myActivities
			returnObj['groupActivities'] = groups
			
			s = json.dumps(returnObj)
			return s
			
		return '{"status":"error", "message":"bad token"}'
	
	
	def getWorkouts(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			startDateList = jsonObj['startDate'].split('-')
			startDate = datetime.date(int(startDateList[0]), int(startDateList[1]), int(startDateList[2]))
			endDateList = jsonObj['endDate'].split('-')
			endDate = datetime.date(int(endDateList[0]), int(endDateList[1]), int(endDateList[2]))
			
			workouts = services.workout_service.getWorkoutsByUserAndDateRange(tlguser, startDate, endDate)
			
			returnObj = {}
			workoutsList = []
			if workouts:
				for  workout in workouts:
					workoutsList.append({'duration':workout.duration, 'key':workout.key.urlsafe()})
					
			returnObj['status'] = 'success'
			returnObj['workouts'] = workoutsList
			s = json.dumps(returnObj)
			return s
			
		return '{"status":"error", "message":"bad token"}'
	
	
	
	
	def getAllWorkouts(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			workouts = services.workout_service.getAllWorkoutsByUser(tlguser)
			
			returnObj = {}
			workoutsList = []
			if workouts:
				for  workout in workouts:
					activities = []
					for activityKey in workout.activities:
						activities.append({'key':activityKey.urlsafe()})
					
					workoutsList.append({
										
										'date':workout.date.strftime('%Y-%m-%d'),
										'duration':workout.duration, 
										'key':workout.key.urlsafe(), 
										'comment':workout.comment,
										'activities':activities
										})
					
			returnObj['status'] = 'success'
			returnObj['workouts'] = workoutsList
			s = json.dumps(returnObj)
			return s
			
		return '{"status":"error", "message":"bad token"}'
	
	
	def getGoogleLoginPage(self):
		url = users.create_login_url()
		returnObj = {}
		returnObj['status'] = 'success'
		returnObj['url'] = url
		s = json.dumps(returnObj)
		
		return s
	
	
	
	
	