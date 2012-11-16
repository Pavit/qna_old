from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from datetime import date, datetime
# from social_auth import __version__ as version
# from social_auth.utils import setting
from models import Question, Answer, Vote
from pprint import pprint
# from social_auth.models import UserSocialAuth
from accounts.models import UserProfile
# from facepy import GraphAPI
from django.db.models import Q
from django.conf import settings
from django.utils import simplejson
from django.core import serializers
from django.contrib.auth.models import User, AnonymousUser



def previous_question(request, previous_question_pk):
	previous_question = Question.objects.get(id = previous_question_pk)
	print previous_question
	context = {
		'previous_question':previous_question,
	}
	return render_to_response("previous_question.html", context, context_instance=RequestContext(request))

def current_question(request, current_question_pk):
	current_question = Question.objects.get(id = current_question_pk)
	context = {
		'current_question':current_question,
	}
	return render_to_response("current_question.html", context, context_instance=RequestContext(request))

def index(request):
	if request.user.is_authenticated():
		user = request.user
		try:
			current_question = Question.objects.filter(~Q(answered_by = user))[:1].get()
		except:
			return redirect('profile')
		try:
			previous_question = request.GET.get('current_question')[0]
		except:
			pass
		# return redirect('poll/polls')
		return render_to_response("results.html", {
			'current_question':current_question,
			'previous_question': previous_question,
			}, context_instance=RequestContext(request))
	else:
		return render_to_response("index.html")

def vote(request, answer_id):
	if request.is_ajax():
		a = Answer.objects.get(id = answer_id)
		previous_question = a.question
		vote = Vote.objects.create(
			question = previous_question,
			ip=request.META['REMOTE_ADDR'],
			answer = a,
			)
		if request.user.is_authenticated():
			grabuser = UserProfile.objects.get(username = request.user.username)
		else:
			grabuser, created = UserProfile.objects.get_or_create(username = "Anonymous", anonymous = True, ip = request.META['REMOTE_ADDR'])
		vote.users.add(grabuser)
		voted_answer = vote.answer
		voted_answer.selected_by.add(grabuser)
		voted_question = vote.question
		voted_question.answered_by.add(grabuser)
		voted_question.save()
		voted_answer.save()
		vote.save()
		current_question = Question.objects.filter(~Q(id = previous_question.id)).order_by('?')[:1].get()
		data = {
			"previous_question_pk":previous_question.id,
			"current_question_pk":current_question.id,
		}
	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

def questions(request):
	if request.user.is_authenticated():
		grabuser = UserProfile.objects.get(username = request.user.username)
	else:
		grabuser, created = UserProfile.objects.get_or_create(username = "Anonymous", anonymous = True, ip = request.META['REMOTE_ADDR'])
	#current_question = Question.objects.filter(~Q(answered_by = grabuser))[:1].get() #----enable this line to prevent repeating questions
	current_question = Question.objects.all().order_by('?')[:1].get()
	context = {'current_question' : current_question,}
	return render_to_response("questions.html", context, context_instance=RequestContext(request))


@login_required
def profile(request):
	user = UserProfile.objects.get(username = request.user.username)
	user.populate_graph_info()
	user.save()
	print user.birthday
	uservotes = user.vote_set.all()
	print uservotes
	pollcount = Poll.objects.all().count()
	print "questions you submit:"
	print user.submissions.all()
	print "questions you answered:"
	print user.answered.all()
	for p in Poll.objects.all():
		print p.tags
	return render_to_response("profile.html", {'user': user, 'pollcount':pollcount,'APP_ID': settings.FACEBOOK_APP_ID}, context_instance = RequestContext(request))

def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return redirect('landing')
