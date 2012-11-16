from django import template
from django.conf import settings
from core.models import *
from core import views
register = template.Library()
from accounts.models import UserProfile

@register.simple_tag(takes_context=True)
def question(context):
    request = context['request']

    try:
        question = Question.published.latest("date")
    except:
        return ''

    if question.get_cookie_name() not in request.COOKIES:
        return views.question(context['request'], question.id).content
    else:
        return views.result(context['request'], question.id).content

@register.simple_tag
def percentage(question, answer):
	question_vote_count = question.get_vote_count()
	if question_vote_count > 0:
		return float(answer.get_vote_count()) / float(question_vote_count) * 100
	else:
		return 0
		
@register.simple_tag()
def votecount(question, answer, userprofile):
	totalquestioncount = 0
	if userprofile.submissions.all().count() > 1:
		for question in userprofile.submissions.all():
			totalquestioncount += question.get_vote_count()
	else:
		try:
			totalquestioncount = userprofile.submissions.all()[0].get_vote_count()
		except IndexError:
			totalquestioncount = 0
	return totalquestioncount