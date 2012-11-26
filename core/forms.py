from models import *
from django.forms import ModelForm
from django import forms
from ajax_select import make_ajax_field

class QuestionForm(ModelForm):
	#question= forms.CharField()
	question  = make_ajax_field(Question,'question','question',help_text="Search for question by name")

	class Meta:
		model = Question
		exclude = ("date", "submitter", "answered_by")

class AnswerForm(ModelForm):
	answer = forms.CharField(label = "")
	
	class Meta:
		model = Answer
		exclude = ('question', 'selected_by',)

