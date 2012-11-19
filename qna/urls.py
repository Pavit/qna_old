from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'core.views.index', name='index'),
    # url(r'^qna/', include('qna.foo.urls')),
	url(r'', include('social_auth.urls')),
	url(r'^questions/$', 'core.views.questions', name='questions'),
	url(r'^vote/(?P<answer_id>\d+)/$', 'core.views.vote', name='vote'),
    url(r'^previous_question/(?P<previous_question_pk>\d+)/$', 'core.views.previous_question', name='previous_question'),
    url(r'^current_question/(?P<current_question_pk>\d+)/$', 'core.views.current_question', name='current_question'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
