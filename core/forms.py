from models import *
from django.forms import ModelForm
from django import forms


class QuestionForm(ModelForm):
	#question= forms.CharField()


	class Meta:
		model = Question
		exclude = ("date", "submitter", "answered_by")

class AnswerForm(ModelForm):
	answer = forms.CharField(label = "")

	class Meta:
		model = Answer
		exclude = ('question', 'selected_by',)

