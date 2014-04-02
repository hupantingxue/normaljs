from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qqcy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^microfront/home/register/', include('register.urls')),
    url(r'^microfront/', include('microfront.urls')),
    url(r'^micromall/', include('micromall.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
