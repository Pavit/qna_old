from models import *
from django.forms import ModelForm
from django import forms


class QuestionForm(ModelForm):
	question= forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'What do you want to ask?'}))


	class Meta:
		model = Question
		exclude = ("date", "submitter", "answered_by", "slug")

class AnswerForm(ModelForm):
	answer = forms.CharField(label = "", widget = forms.TextInput(attrs={'placeholder': "What kind of answer do you want?"}))

	class Meta:
		model = Answer
		exclude = ('question', 'selected_by',)

