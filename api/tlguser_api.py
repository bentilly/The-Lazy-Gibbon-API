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
				for groupAdmin in groupAdmins:
					group = groupAdmin.group.get()
					groupList.append({'name':group.name, 'key':group.key.urlsafe()})
			
			returnObj['status'] = 'success'
			returnObj['adminGroups'] = groupList
			s = json.dumps(returnObj)
			return s
			
		else:
			return '{"status":"error", "message":"invalid token"}'
		
		
	def getActivites(self, jsonObj):
		#Authentication: Valid TOKEN
		tlguser = services.token_service.getUserFromToken(jsonObj['token'])
		
		if tlguser:
			activities = services.activity_service.getActivities(tlguser)
			
			returnObj = {}
			activitiesList = []
			if activities:
				for  activity in activities:
					activitiesList.append({'name':activity.name, 'key':activity.key.urlsafe(), 'colour':activity.colour})
			
			returnObj['status'] = 'success'
			returnObj['activities'] = activitiesList
			
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
	
	
	
	
	