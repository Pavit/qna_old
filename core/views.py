from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from datetime import date, datetime
from models import Question, Answer, Vote
from pprint import pprint
from accounts.models import UserProfile
from facepy import GraphAPI
from django.db.models import Q
from django.conf import settings
from django.utils import simplejson
from django import forms
from django.core import serializers
from django.contrib.auth.models import User, AnonymousUser
from forms import *
from django.shortcuts import get_object_or_404
from random import randrange
from django.views.decorators.csrf import csrf_exempt
def test (request):
	return render_to_response("test.html")

def previous_question(request, previous_question_pk):
	previous_question = Question.objects.get(id = previous_question_pk)
	resp = {
		'previous_question': previous_question,
	}
	# answer_list =[]
	# answer_list.append(["Answer", "Votes"])
	# for a in previous_question.answer_set.all():
	# 	answer_list.append([a.answer, a.get_vote_count()])
	# resp["answers"] = answer_list
	#data = simplejson.dumps(resp)
	#return HttpResponse(data, mimetype = "application/json")
	return render_to_response("previous_question.html", resp, context_instance=RequestContext(request))

def current_question(request, current_question_pk):
	current_question = Question.objects.get(id = current_question_pk)
	next_question = Question.objects.filter(~Q(id = current_question.id)).order_by('?')[:1].get()
	answer_dict = {}
	for a in current_question.answer_set.all():
		answer_dict[a.id] = a.answer
	response_dict = {
		'current_question_title':current_question.question,
		'current_question_choices': answer_dict,
		'current_question': current_question,
		'next_question': next_question,
	}
	#data = simplejson.dumps(response_dict)
	#return HttpResponse(data, mimetype = "application/json")
	return render_to_response("current_question.html", response_dict)#, context_instance=RequestContext(request))

def view_question(request, slug, id):
	current_question = get_object_or_404(Question, pk = id)
	return render_to_response("questions.html", {'current_question':current_question})

@csrf_exempt
def index(request):
	if request.user.is_authenticated():
		print request.user.userprofile
		user = request.user.userprofile
		user.fb_access_token = request.user.social_auth.get(provider='facebook').extra_data["access_token"]
		print user.fb_access_token
		user.populate_graph_info()
		user.save()
		print user.gender
		return redirect(questions)
		#return render_to_response("questions.html", {},)
	# 	user = request.user
	# 	try:
	# 		current_question = Question.objects.filter(~Q(answered_by = user))[:1].get()
	# 	except:
	# 		return redirect('profile')
	# 	try:
	# 		previous_question = request.GET.get('current_question')[0]
	# 	except:
	# 		previous_question = None
	# 	# return redirect('poll/polls')
	# 	return render_to_response("questions.html", {
	# 		'current_question':current_question,
	# 		'previous_question': previous_question,
	# 		}, context_instance=RequestContext(request))
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

		print dir(request.user)
		print request.user.is_authenticated()
		user = request.user
		print user.userprofile
		if request.user.is_authenticated():
			grabuser = request.user.userprofile
			print grabuser
		else:
			grabuser, created = UserProfile.objects.get_or_create(username = "Anonymous", anonymous = True, ip = request.META['REMOTE_ADDR'], user_id = randrange(10))
		vote.users.add(grabuser)
		voted_answer = vote.answer
		voted_answer.selected_by.add(grabuser)
		voted_question = vote.question
		voted_question.answered_by.add(grabuser)
		voted_question.save()
		voted_answer.save()
		vote.save()
		grabuser.save()
		print grabuser.selection.all()
		current_question = Question.objects.filter(~Q(id = previous_question.id)).order_by('?')[:1].get()
		answer_list =[]
		answer_list.append(["Answer", "Votes"])
		for a in previous_question.answer_set.all():
			answer_list.append([a.answer, a.get_vote_count()])
		#resp["answers"] = answer_list
		data = {
			"previous_question_pk":previous_question.id,
			"current_question_pk":current_question.id,
			"previous_question":previous_question.question,
			"previousanswers": answer_list,

		}
	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

def questions(request):
	if request.user.is_authenticated():
		grabuser = request.user
	else:
		grabuser, created = UserProfile.objects.get_or_create(username = "Anonymous", anonymous = True, ip = request.META['REMOTE_ADDR'],user_id = randrange(10))
	#current_question = Question.objects.filter(~Q(answered_by = grabuser))[:1].get() #----enable this line to prevent repeating questions
	current_question = Question.objects.all().order_by('?')[:1].get()

	context = {'current_question' : current_question,}
	return render_to_response("questions.html", context, context_instance=RequestContext(request))

# def navigation_autocomplete(request, template_name='autocomplete.html'):
#     q = request.GET.get('q', '')
#     context = {'q': q}
#     queries = {}
#     queries['questions'] = Question.objects.filter(
#         Q(question__icontains=q))
#     queries['answers'] = Answer.objects.filter(answer__icontains=q)
#     context.update(queries)
#     return shortcuts.render(request, template_name, context)#, context_instance=RequestContext(request))

@login_required
def profile(request):

	user = request.user.userprofile
	#user.populate_graph_info()
	user.save()
	print user.birthday
	uservotes = user.vote_set.all()
	print uservotes
	pollcount = Question.objects.all().count()
	print "questions you submit:"
	print user.submissions.all()
	print "questions you answered:"
	print user.answered.all()
	totalvotes = 0
	for q in user.submissions.all():
		totalvotes += q.get_vote_count()
	return render_to_response("profile.html", {'pollcount':pollcount,'APP_ID': settings.FACEBOOK_APP_ID, 'totalvotes':totalvotes,}, context_instance = RequestContext(request))

def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return redirect('index')

def search_form(request):
	return render_to_response("search_form.html")

def search_results(request, searchtext):
	print "Search results"
	response_dict = {
		'results':Question.objects.filter(Q(question__icontains=searchtext)).order_by('question'),
	}

	return render_to_response("search_results.html", response_dict)


def search(request):
	data = {}
	print request.GET
	if 'searchtext' in request.GET:
		q = request.GET.get('searchtext')
		json = serializers.serialize('json', Question.objects.filter(Q(question__icontains=q)).order_by('question'))
	# 	q = request.GET.get('searchtext')
	# 	for question in Question.objects.filter(Q(question__icontains=q)).order_by('question'):
	# 		data[question.question] = question
	# ser = serializers.serialize(data)
	# json = simplejson.dumps(ser)
	print json
	return HttpResponse(json, mimetype='application/json')
    # dd = {}
    # if 'question' in request.GET:
    #     dd['entered'] = request.GET.get('question')
    # initial = {'question':"\"This is an initial value,\" said O'Leary."}
    # form = QuestionForm(initial=initial)
    # dd['form'] = form
    # return render_to_response('search_form.html',dd,context_instance=RequestContext(request))

from core.forms import *
from django.core.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
@login_required
def submitquestion(request):
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = False
				
	AnswerFormSet = formset_factory(AnswerForm, max_num=5, formset = RequiredFormSet)
	user = request.user.userprofile
	if request.method == 'POST': # If the form has been submitted...
		print "this poll should be assigned to: %s" %user
		question_form = QuestionForm(request.POST) # A form bound to the POST data
		# Create a formset from the submitted data
		answer_formset = AnswerFormSet(request.POST, request.FILES)
		if question_form.is_valid() and answer_formset.is_valid():
			print "made it past valid check"
			question = question_form.save(commit=False)
			question.submitter = user
			question.save()
			print answer_formset
			#print poll.customuser.username
			for form in answer_formset.forms:
				answer = form.save(commit=False)
				answer.question = question
				answer.save()
				print answer
			return redirect('profile')
	else:
		question_form = QuestionForm()
		answer_formset = AnswerFormSet()
	c = {'question_form': question_form,
	'answer_formset': answer_formset,
	}
	c.update(csrf(request))
	return render_to_response('submitquestion.html', c, context_instance = RequestContext(request))