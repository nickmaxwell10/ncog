from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ncog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'core.views.login', name='login'),
    url(r'^home/$', 'core.views.home', name='home'),
    url(r'^friends/$', 'core.views.friends', name='friends'),
    url(r'^scores/$', 'core.views.scores', name='scores'),

    #Facebook
    (r'^facebook/', include('django_facebook.urls')),
	(r'^accounts/', include('django_facebook.auth_urls')), #Don't add this line if you use django registration or userena for registration and auth.

    url(r'^admin/', include(admin.site.urls)),
)
