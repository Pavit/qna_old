from django.conf.urls import patterns, include, url
from django.conf import settings


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'core.views.index', name='index'),
    url(r'^(?P<slug>[-\w\d]+),(?P<id>\d+)/$', 'core.views.view_question', name='view_question'),
    # url(r'^qna/', include('qna.foo.urls')),
	url(r'', include('social_auth.urls')),
	url(r'^logout/$', 'core.views.logout', name='logout'),
	url(r'^questions/$', 'core.views.questions', name='questions'),
	url(r'^profile/$', 'core.views.profile', name='profile'),
	url(r'^submitquestion/$', 'core.views.submitquestion', name='submitquestion'),
    url(r'^search/$', 'core.views.search', name='search'),
    url(r'^search_results/(?P<searchtext>\w+)/$', 'core.views.search_results', name='search_results'),
	url(r'^vote/(?P<answer_id>\d+)/$', 'core.views.vote', name='vote'),
    url(r'^previous_question/(?P<previous_question_pk>\d+)/$', 'core.views.previous_question', name='previous_question'),
    url(r'^current_question/(?P<current_question_pk>\d+)/$', 'core.views.current_question', name='current_question'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_form',  'core.views.search_form',name='search_form'),
    url(r'^test',  'core.views.test',name='test'),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)
urlpatterns += staticfiles_urlpatterns()