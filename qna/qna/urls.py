from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^test/$', 'core.views.test'),
    url(r'^$', 'core.views.index', name='index'),
    # url(r'^qna/', include('qna.foo.urls')),
	url(r'', include('social_auth.urls')),
	url(r'^questions/$', 'core.views.questions', name='questions'),
	url(r'^vote/(?P<answer_id>\d+)/$', 'core.views.vote', name='vote'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
