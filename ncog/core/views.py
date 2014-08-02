from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from open_facebook import OpenFacebook
import json

# Create your views here.
def login(request):
    context = RequestContext(request)

    return render_to_response('core/login.html', context)

def home(request):
    context = RequestContext(request)

    access_token = request.user.access_token

    facebook = OpenFacebook(access_token)
    inbox = facebook.get('/me/inbox')
    
    context['inbox'] = inbox

    return render_to_response('core/home.html', context)
