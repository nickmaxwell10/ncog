from celery import shared_task
from django.conf import settings
from open_facebook import OpenFacebook
import json
from bson import ObjectId
import pymongo as pymongo
from pymongo import Connection

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
	
	

	
	to_return = ""
	for conversation in inbox['data']:
		if 'comments' in conversation and 'data' in conversation['comments']:
					thread_participants = conversation['to']['data']
					if (len(thread_participants) == 2):
						
						for participant in thread_participants:
							participant = int(participant['id'])
							if (user.facebook_id != participant):
								other_id = participant
								
							#print "user id " , user.faceid 
						#individual converation loop
						message_total = 0
						#for conversation in inbox['paging']
						for comment in conversation['comments']['data']:

							if 'from' in comment and 'id' in comment['from'] and 'id' in comment and 'message' in comment and 'created_time' in comment:
									if int(comment['from']['id']) == user.facebook_id:
										message = {
											"user_id": user.facebook_id,
											"to_id": other_id,
											"from_id": comment['from']['id'],
											"message_id": comment['id'],
											"message": comment['message'],
											"date": comment['created_time']
										}
										db.messages.insert(message)
										message_total = message_total + 1
										print "from me to ", other_id
									
									else:
										
										message = {
											"user_id": user.facebook_id,
											"to_id": user.facebook_id,
											"from_id": comment['from']['id'],
											"message_id": comment['id'],
											"message": comment['message'],
											"date": comment['created_time']
										}
										db.messages.insert(message)
										message_total = message_total + 1
										print "from  ", other_id, " to me " , "my id = ", user.facebook_id
						
						if message_total == 25:
							url = conversation['comments']['paging']['next']
							url = url.split("v2.0")[1]
							
							#depthlooper(inbox, user, facebook, url)
						


	return inbox

#def depthlooper( user, facebook, url):
	#print facebook.get(url)


