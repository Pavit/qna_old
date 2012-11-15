from django.contrib import admin
from core.models import *
from django.utils.translation import gettext as _

class QuestionAnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    max_num = 5

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'date', 'submitter',)
    inlines = [QuestionAnswerInline,]

admin.site.register(Question, QuestionAdmin)


# class VoteAdmin(admin.ModelAdmin):
#     list_display = ('poll', 'ip', 'user', 'datetime')
#     list_filter = ('poll', 'datetime')
#
# admin.site.register(Vote, VoteAdmin)
