from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from datetime import date, datetime
from social_auth import __version__ as version
from social_auth.utils import setting
from poll.models import Poll, Item
from pprint import pprint
from social_auth.models import UserSocialAuth
from core.models import CustomUser
from facepy import GraphAPI
from django.db.models import Q
from django.conf import settings

