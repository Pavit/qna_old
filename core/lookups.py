from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from core.models import *


class QuestionLookup(LookupChannel):

    model = Question

    def check_auth(self, request):
        return True

    def get_query(self,q,request):
        return Question.objects.filter(Q(question__icontains=q)).order_by('question')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.question

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s" % (escape(obj.question))