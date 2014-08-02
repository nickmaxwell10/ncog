from celery import shared_task
from django.conf import settings
from open_facebook import OpenFacebook
import json

# @shared_task
def getUserInbox(user):
	access_token = user.access_token
	facebook = OpenFacebook(access_token)
	inbox = facebook.get('/me/inbox')
	
	return inbox