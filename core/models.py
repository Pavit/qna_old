import datetime
from django.db import models
from django.utils.translation import gettext as _
from accounts.models import UserProfile
from django.db.models.manager import Manager
from django.core.exceptions import ValidationError
#from tagging_autocomplete_tagit.models import TagAutocompleteTagItField

class Question(models.Model):
	question = models.CharField(max_length = 250)
	date = models.DateField(default=datetime.date.today)
	submitter = models.ForeignKey(UserProfile, null=True, blank=True, default=None, related_name='submissions')
	answered_by = models.ManyToManyField(UserProfile, null=True, blank=True, default=None, related_name = 'answered')
	slug = models.SlugField(blank = True, null=True)
	#tags = TagAutocompleteTagItField(max_tags=False)

	class Meta:
		ordering = ['-date']
		verbose_name = _('question')
		verbose_name_plural = _('questions')

	def __unicode__(self):
		return self.question

	def get_vote_count(self):
		return Vote.objects.filter(question=self).count()

	vote_count = property(fget=get_vote_count)


class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length = 250)
	selected_by = models.ManyToManyField(UserProfile, null=True, blank=True, default=None, related_name = 'selection')

	class Meta:
		verbose_name = _('answer')
		verbose_name_plural = _('answers')

	def __unicode__(self):
		return u'%s' % (self.answer,)

	def get_vote_count(self):
		return Vote.objects.filter(answer=self).count()

	def get_vote_count_male(self):
		return self.selected_by.filter(gender="male").count()

	def get_vote_count_female(self):
		return self.selected_by.filter(gender="female").count()

	vote_count = property(fget=get_vote_count)
	vote_count_male = property(fget=get_vote_count_male)
	vote_count_female = property(fget=get_vote_count_female)

class Vote(models.Model):
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer)
	ip = models.IPAddressField(verbose_name=_('user\'s IP'))
	users = models.ManyToManyField(UserProfile)
	datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('vote')
		verbose_name_plural = _('votes')
