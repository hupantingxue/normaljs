from django.conf.urls import patterns, url

from micromall import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^(.*).js$',views.js_resource),
    url(r'^(.*).css$',views.css_resource),
    url(r'^(.*).gif$',views.gif_resource),
    url(r'^(.*).png$',views.png_resource),
    url(r'^(.*).jpg$',views.jpg_resource),
)
