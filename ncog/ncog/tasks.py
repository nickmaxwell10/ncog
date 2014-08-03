from __future__ import absolute_import, division

from celery import shared_task
from django.conf import settings
from open_facebook import OpenFacebook
import json
from bson import ObjectId
import pymongo as pymongo
from pymongo import Connection
from datetime import datetime

db = Connection(
    host=getattr(settings, "MONGODB_HOST", None),
    port=getattr(settings, "MONGODB_PORT", None)
)[settings.MONGODB_DATABASE]

if getattr(settings, "MONGODB_USERNAME", None):
    db.authenticate(getattr(settings, "MONGODB_USERNAME", None), getattr(settings, "MONGODB_PASSWORD", None))


# def getUserInbox(user):
# 	access_token = user.access_token
# 	facebook = OpenFacebook(access_token)

# 	nextConversationUrl = 'me/inbox'
# 	numMessages = 1
# 	while(numMessages > 0):
# 		numMessages = 0
# 		conversations = facebook.get(nextConversationUrl)
# 		for conversation in conversations:
# 			for message in conversation.messages:
# 				numMessages++
# 		nextConversationUrl = conversations.pager.next


@shared_task
def getUserInbox(user):
	access_token = user.access_token
	facebook = OpenFacebook(access_token)
	inbox = facebook.get('/me/inbox')
	inbox2 = facebook.get(inbox['paging']['next'].split("v2.0")[1])
	#to_return = dict(breadthlooper(inbox, user, facebook).items()  + breadthlooper(inbox2, user, facebook).items())
	#print to_return
	return(breadthlooper(inbox,user, facebook) , breadthlooper(inbox2,user, facebook))

def breadthlooper( inbox, user, facebook):
	for conversation in inbox['data']:
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
								
							#print "user id " , user.faceid 
						#individual converation loop
						message_total = 0
						#for conversation in inbox['paging']
						for comment in conversation['comments']['data']:

							if 'from' in comment and 'id' in comment['from'] and 'id' in comment and 'message' in comment and 'created_time' in comment:
									date_object = datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000')

									if int(comment['from']['id']) == user.facebook_id:
										message = {
											"user_id": user.facebook_id,
											"to_id": other_id,
											"to_me" : False,
											"from_id": comment['from']['id'],
											"message_id": comment['id'],
											"message": comment['message'],
											"date": date_object,
										}
										db.messages.insert(message)
										message_total = message_total + 1
										
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
										message_total = message_total + 1
										
						
						#if message_total == 25:
							#url = conversation['comments']['paging']['next']
							#url = url.split("v2.0")[1]
							
							#depthlooper(inbox, user, facebook, url)
						

	db.user_friends.update(
							{"user_id": user.facebook_id},
							{"$set": { "status": "complete" }}
						)
	return inbox

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




