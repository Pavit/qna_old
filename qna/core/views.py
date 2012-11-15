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


def test(request):
	response_string="hello"
	print response_string
	return HttpResponse(response_string,mimetype='text/plain')


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
	message = {"previous_question": ""}
	if request.is_ajax():
		print "ajax request"
		answer = Answer.objects.get(id = answer_id)
		print "answer selected was: %s" %answer
		previous_question = answer.question
		print "Question just answered: %s" %previous_question
		current_question = Question.objects.filter(~Q(id = previous_question.id)).order_by('?')[:1].get()
		print "Next question up is: %s" %current_question
		message = {
			'previous_question':previous_question,
			'current_question':current_question,
		}
	else:
		message = "no data"
	json = simplejson.dumps(message)
	return HttpResponse(json, mimetype='application/json')

def questions(request):
	# user = request.user
	# if request.method == "POST":
	# 	print "request is post!"
	# 	if request.is_ajax():
	# 		resp = dict()
			
	# 		print "request is ajax!"
	# 	else:
	# 		print "request is NOT AJAX"
	# 	answer_pk = request.POST.get("answer", False)
	# 	print answer_pk
	# 	if user.is_authenticated():
	# 		current_question = Question.objects.filter(~Q(answered_by = user))[:1].get()
	# 	else:
	# 		current_question = Question.objects.order_by('?')[:1].get()
	# 	context = {
	# 		'current_question':current_question,
	# 	}
	# 	return render_to_response("questions.html", context, context_instance=RequestContext(request))
	user = request.user
	if user.is_authenticated():
		current_question = Question.objects.filter(~Q(answered_by = user))[:1].get()
	else:
		current_question = Question.objects.order_by('?')[:1].get()
		print Question.objects.all()
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
