from __future__ import absolute_import, division
from celery import shared_task
from django.conf import settings
from open_facebook import OpenFacebook
import json
from bson import ObjectId
import pymongo as pymongo
from pymongo import Connection
from datetime import datetime

from ncog.predictor import calculate_scores

db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]

if getattr(settings, "MONGODB_USERNAME", None):
    db.authenticate(getattr(settings, "MONGODB_USERNAME", None), getattr(settings, "MONGODB_PASSWORD", None))



@shared_task
def getUserInbox(user):
	access_token = user.access_token
	facebook = OpenFacebook(access_token)
	inbox = facebook.get('/me/inbox')
	inbox2 = facebook.get(inbox['paging']['next'].split("v2.0")[1])
	
	return breadthlooper(inbox,user, facebook)

def breadthlooper( inbox, user, facebook):
	combined_list = []
	list_to = []
	list_from = []
	combined_list = []
	print "breadthlooper starting"
	for conversation in inbox['data']:
		other_id = None
		list_to = []
		list_from = []
		if 'comments' in conversation and 'data' in conversation['comments']:
					thread_participants = conversation['to']['data']
					if (len(thread_participants) == 2):
						
						for participant in thread_participants:
							participant_id = int(participant['id'])
							if (user.facebook_id != participant_id):
								other_id = participant_id
								if db.user_friends.find_one({"user_id": user.facebook_id}):
									db.user_friends.update(
										{"user_id": user.facebook_id},
										{"$addToSet" : {"friends" : {"user_id": other_id, "name": participant['name']}}}
										)
									db.user_friends.update(
										{"user_id": user.facebook_id},
										{"$set": { "status": "processing" }}
										)
								else:
										db.user_friends.insert({
											"user_id": user.facebook_id,
											"status": "processing",
											"friends" : [
												{
												"user_id": other_id, 
												"name": participant['name']
												}
											]
										}
										)
						

						list_to.append(scoreThreadMe(user.facebook_id, str(other_id)))
						list_from.append(scoreThreadYou(user.facebook_id, str(other_id)))
						combined_list.append(combinedThread(str(user.facebook_id), str(other_id)))
						
						for comment in conversation['comments']['data']:

							if 'from' in comment and 'id' in comment['from'] and 'id' in comment and 'message' in comment and 'created_time' in comment:
									date_object = datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
									print "running db writes with new conversions"
									if int(comment['from']['id']) == user.facebook_id:
										message = {
											"user_id":user.facebook_id,
											"to_id": other_id,
											"to_me" : False,
											"from_id": comment['from']['id'],
											"message_id": comment['id'],
											"message": comment['message'],
											"date": date_object,
										}
										db.messages.insert(message)

										
									else:
										message = {
											"user_id": user.facebook_id,
											"to_id": user.facebook_id,
											"to_me": True,
											"from_id": comment['from']['id'],
											"message_id": comment['id'],
											"message": comment['message'],
											"date": date_object,
										}
										db.messages.insert(message)

						conversation_score = calculate_scores(combined_list, list_to, list_from, user.facebook_id, other_id)
						db.conversation_score.insert(conversation_score)



	db.user_friends.update(
							{"user_id": user.facebook_id},
							{"$set": { "status": "complete" }})

	print '---ABOUT TO CALCULATE SCORES'
	
	return True



def getFriends(user_id):
	user_friend = db.user_friends.find_one({"user_id":user_id})
	if user_friend:
		if user_friend['status'] == "complete":
			return {
						"status": "complete",
						"friends": user_friend['friends']
				   }
		else:
			return "processing"
	else:
		return "processing"

def getScores(user_id):
	user_scores = db.conversation_score.find({"user_id":user_id})
	scores = []
	for score in user_scores:
		score['_id'] = str(score['_id'])
		scores.append(score)

	return scores


def scoreThreadMe(user_id, other_id):
	#pulls messages from thread of other person to user

	to_return = []
	messages = db.messages.find({ "from_id":other_id, "user_id":user_id})
								
	for message in messages:
		to_return.append(message)

	
	return(to_return)



def scoreThreadYou(user_id, other_id):
	#pulls messages from thread of user to other person
	print "running scoreThreadYou"
	to_return = []
	messages = db.messages.find({ "to_id": other_id, "user_id":user_id })
				
	for message in messages:
		print "match"
		to_return.append(message)

	

	return(to_return)

def combinedThread(user_id, other_id):
	print "combinedThread running" 
	to_return = []



	messages = db.messages.find(
							{"user_id": user_id,
							 "$or": [
									{ "to_id": other_id},
									{ "from_id" : other_id},
								]
							}).sort([("date", 1)])
				
	for message in messages:

	
		to_return.append(message)
	return(to_return)




