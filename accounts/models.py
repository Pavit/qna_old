# Define a custom User class to work with django-social-auth
from django.db import models
from facepy import GraphAPI
import time, datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends import google
from social_auth.signals import socialauth_registered

# class UserProfileManager(models.Manager):
# 	def create_user(self, username, email):
# 		return self.model._default_manager.create(username=username)


class Education(models.Model):
	school_id = models.CharField(max_length=200, blank=True, null=True)
	school_name = models.CharField(max_length=200, blank=True, null=True)
	school_type = models.CharField(max_length=200, blank=True, null=True)
	year = models.CharField(max_length=200, blank=True, null=True)

class Concentration(models.Model):
	conc_id = models.CharField(max_length=200, blank=True, null=True)
	conc_name = models.CharField(max_length=200, blank=True, null=True)
	education = models.ForeignKey(Education)
	
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	username = models.CharField(max_length=128, unique=False, blank=True, null=True)
	anonymous = models.BooleanField()
	ip = models.IPAddressField(verbose_name=('user\'s IP'), null=True, blank=True)
	full_name = models.CharField(max_length=128, unique=True, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	last_login = models.DateTimeField(blank=True, null=True)
	fb_id = models.CharField(max_length=200, null=True, blank = True)
	fb_access_token = models.CharField(max_length=200, null = True, blank = True)
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	locale = models.CharField(max_length=200, blank=True, null=True)
	#gender = models.CharField(max_length=200, blank=True, null=True)
	hometown = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	work_position_id = models.CharField(max_length=200, blank=True, null=True)
	work_position_name = models.CharField(max_length=200, blank=True, null=True)
	work_start_date = models.CharField(max_length=200, blank=True, null=True)
	work_location_id = models.CharField(max_length=200, blank=True, null=True)
	work_location_name = models.CharField(max_length=200, blank=True, null=True)
	work_employer_id = models.CharField(max_length=200, blank=True, null=True)
	work_employer_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	updated_time = models.DateTimeField(blank=True, null=True)
	birthday = models.DateTimeField(blank=True, null=True)
	timezone = models.CharField(max_length=200, blank=True, null=True)
	educations = models.ManyToManyField(Education)
	friends = models.ManyToManyField('self')
	age = models.IntegerField(blank=True, null=True)
	
	# objects = UserProfileManager()
	# def is_authenticated(self):
	# 	return True

	def populate_graph_info(self):
		graphinfo = GraphAPI(self.fb_access_token).get('me/')
		if "name" in graphinfo: self.username = graphinfo["name"]
		if "first_name" in graphinfo: self.first_name = graphinfo["first_name"]
		if "last_name" in graphinfo: self.last_name = graphinfo["last_name"]
		if "gender" in graphinfo: self.gender = graphinfo["gender"]
		if "email" in graphinfo: self.email = graphinfo["email"]
		if "birthday" in graphinfo:
			self.birthday = datetime.datetime.strptime(graphinfo["birthday"], "%m/%d/%Y")
		if "timezone" in graphinfo: self.timezone = graphinfo["timezone"]
		if "hometown" in graphinfo: self.hometown = graphinfo["hometown"]
		if "location" in graphinfo: self.location = graphinfo["location"]
		if "work" in graphinfo:
			self.work_position_id = graphinfo["work"][0]["position"]["id"]
			self.work_position_name = graphinfo["work"][0]["position"]["name"]
			self.work_start_date = graphinfo["work"][0]["start_date"]
			self.work_location_id = graphinfo["work"][0]["location"]["id"]
			self.work_location_name = graphinfo["work"][0]["location"]["name"]
			self.work_employer_id = graphinfo["work"][0]["employer"]["id"]
			self.work_employer_name = graphinfo["work"][0]["employer"]["name"]
		if "education" in graphinfo:
			for item in graphinfo["education"]:
				newed = Education.objects.create()
				if "school" in item:
					newed.school_id = item["school"]["id"]
					newed.school_name = item["school"]["name"]
				if "type" in item: newed.school_type = item["type"]
				if "year" in item: newed.year = item["year"]["name"]
				newed.save()
				print item
				if "concentration" in item:
					for conc in item["concentration"]:
						newconc = Concentration.objects.create(education = newed)
						newconc.conc_id = conc["id"]
						newconc.conc_name = conc["name"]
						newconc.save()
				newed.save()
				self.educations.add(newed)
		self.save()
		return self

	def check_friends(self):
		friendlist = GraphAPI(self.fb_access_token).get('me/friends')
		frienddict = friendlist["data"]
		#check if user's friends are already members of the site
		compare_list = []
		user_fb_ids = UserProfile.objects.values_list('fb_id', flat=True).order_by('fb_id')
		friend_fb_ids = []
		for friend in frienddict:
			friend_fb_ids.append(friend["id"])
			matches = UserProfile.objects.filter(fb_id__in=friend_fb_ids)
		try:
			for match in matches:
				self.friends.add(match)
		except:
			pass
		#for match in list(set(user_fb_ids).intersection(set(friend_fb_ids))):
		#matched_friend = UserProfile.objects.get(fb_id = match)
			#self.friends.add(matched_friend)
		self.save()
		return self
		
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in UserProfile._meta.fields]

		
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
		
		
#from social_auth.backends.facebook import FacebookBackend
#from social_auth.signals import socialauth_registered

#def new_users_handler(sender, user, response, details, **kwargs):
#    user.is_new = True
#    if user.is_new:
#		user.userprofile.populate_graph_info()
#		user.save()
 #   return True
 
#socialauth_registered.connect(new_users_handler, sender=None)