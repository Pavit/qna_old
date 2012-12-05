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
from django import forms
from django.core import serializers
from django.contrib.auth.models import User, AnonymousUser
from forms import *

def test (request):
	return render_to_response("test.html")

def previous_question(request, previous_question_pk):
	previous_question = Question.objects.get(id = previous_question_pk)
	resp = {
		'previous_question': previous_question.question,
	}
	answer_list =[]
	answer_list.append(["Answer", "Votes"])
	for a in previous_question.answer_set.all():
		answer_list.append([a.answer, a.get_vote_count()])
	resp["answers"] = answer_list
	data = simplejson.dumps(resp)
	return HttpResponse(data, mimetype = "application/json")
	#return render_to_response("previous_question.html", {"data": resp, "previous_question":previous_question})

def current_question(request, current_question_pk):
	current_question = Question.objects.get(id = current_question_pk)
	answer_dict = {}
	for a in current_question.answer_set.all():
		answer_dict[a.id] = a.answer
	response_dict = {
		'current_question_title':current_question.question,
		'current_question_choices': answer_dict,
		'current_question': current_question,
	}
	#data = simplejson.dumps(response_dict)
	#return HttpResponse(data, mimetype = "application/json")
	print current_question.get_absolute_url()
	return render_to_response("current_question.html", response_dict)#, context_instance=RequestContext(request))

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
	uservotes = user.vote_set.all()
	pollcount = Poll.objects.all().count()

	return render_to_response("profile.html", {'user': user, 'pollcount':pollcount,'APP_ID': settings.FACEBOOK_APP_ID}, context_instance = RequestContext(request))

def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return redirect('landing')

def search_form(request):
	return render_to_response("search_form.html")

def search_results(request):
	if 'searchtext' in request.GET:
		q = request.GET.get('searchtext')
		results =  Question.objects.filter(Q(question__icontains=q))
	return render_to_response("search_results.html", {'results':results})
	
def submit(request):
	return render_to_response("submit.html")

def search(request):
	data = {}
	print request.GET
	if 'searchtext' in request.GET:
		q = request.GET.get('searchtext')
		queryset =  Question.objects.filter(Q(question__icontains=q))
		search_list = []
		for question in queryset:
			search_list.append({'question': question.question, 'url':question.get_absolute_url()})
		json = simplejson.dumps(search_list)
		#json = serializers.serialize('json', queryset, indent = 4, extras=('get_absolute_url'))
		return HttpResponse(json, mimetype='application/json')
	return HttpResponse(json, mimetype='application/json')