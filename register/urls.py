from django.conf.urls import patterns, url

from register import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<open_id>\w+)/$', views.detail, name='detail'),
)
