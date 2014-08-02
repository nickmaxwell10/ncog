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

# @shared_task
def getUserInbox(user):
	access_token = user.access_token
	facebook = OpenFacebook(access_token)
	inbox = facebook.get('/me/inbox')

	for thread in inbox['data']:
		if 'comments' in thread and 'data' in thread['comments']:
			for comment in thread['comments']['data']:
				if 'from' in comment and 'id' in comment['from'] and 'message' in comment and 'created_time' in comment:
					message = {
						"user_id": user.facebook_id,
						"from_id": comment['from']['id'],
						"message": comment['message'],
						"date": comment['created_time']
					}
					db.messages.insert(message)
	
	return inbox