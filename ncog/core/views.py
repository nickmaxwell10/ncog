from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from open_facebook import OpenFacebook
import json

from ncog.tasks import getUserInbox, getFriends, getScores
# Create your views here.
def login(request):
    context = RequestContext(request)

    return render_to_response('core/login.html', context)

def home(request):
    context = RequestContext(request)
    user = request.user
    getUserInbox.delay(user)

    context['user'] = user.facebook_name
    context['gender'] = user.gender

    return render_to_response('core/home.html', context)


def friends(request):
    context = RequestContext(request)

    friends = getFriends(request.user.facebook_id)

    data = json.dumps(friends)

    return HttpResponse(data, mimetype='application/json')

def scores(request):
    context = RequestContext(request)

    scores = getScores(request.user.facebook_id)

    data = json.dumps(scores)

    return HttpResponse(data, mimetype='application/json')