from django.conf.urls import patterns, url

from microfront import views

urlpatterns = patterns('',
    url(r'^home/register/(?P<open_id>\w+)$', views.register, name='register'),
    url(r'^orders/add/(?P<order_id>\d+)$', views.order_add, name='order'),
    url(r'^orders/export$', views.order_export, name='order_export'),
    url(r'^orders/date$', views.order_querydate, name='order_querydate'),
    url(r'^orders/shoppinglist$', views.order_shoplist, name='order_shoplist'),
    url(r'^orders/save/$', views.order_save, name='order_save'),
    url(r'^orders/del/$', views.order_del, name='order_del'),
    url(r'^users/save/$', views.user_save, name='user_save'),
    url(r'^users/del/$', views.user_del, name='user_del'),
    url(r'^users/query/$', views.user_query, name='user_query'),
    url(r'^customers/edit/(?P<open_id>\w+)$', views.cedit, name='customer_edit'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^addr/$', views.save_addr, name='addr'),
    url(r'^dltime/$', views.save_dltime, name='dltime'),
    url(r'^$', views.index, name='index'),
    url(r'^(.*).js$',views.js_resource),
    url(r'^(.*).css$',views.css_resource),
    url(r'^(.*).gif$',views.gif_resource),
    url(r'^(.*).png$',views.png_resource),
    url(r'^(.*).jpg$',views.jpg_resource),
    url(r'^(.*).json$',views.json_resource),
)
