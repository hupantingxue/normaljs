from django.conf.urls import patterns, url

from microfront import views

urlpatterns = patterns('',
    url(r'^orders/add/(?P<order_id>\d+)$', views.order_add, name='order'),
    url(r'^orders/export$', views.order_export, name='order_export'),
    url(r'^customers/edit/(?P<open_id>\w+)$', views.cedit, name='customer_edit'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^$', views.index, name='index'),
    url(r'^(.*).js$',views.js_resource),
    url(r'^(.*).css$',views.css_resource),
    url(r'^(.*).gif$',views.gif_resource),
    url(r'^(.*).png$',views.png_resource),
    url(r'^(.*).jpg$',views.jpg_resource),
    url(r'^(.*).json$',views.json_resource),
)
