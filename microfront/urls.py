from django.conf.urls import patterns, url

from microfront import views

urlpatterns = patterns('microfront.views',
    url(r'^login/$', views.mylogin, name='login'),
    url(r'^logout/$', views.mylogout, name='logout'),
    url(r'^home/register/(?P<open_id>\w+)$', views.register, name='register'),
    url(r'^home/register/(?P<open_id>\w+)$', views.register, name='register'),
    url(r'^home/login/(?P<open_id>\w+)$', views.home_login, name='homelogin'),
    url(r'^orders/add/(?P<order_id>\d+)$', views.order_add, name='order'),
    url(r'^orders/export/$', views.order_export, name='order_export'),
    url(r'^orders/date$', views.order_querydate, name='order_querydate'),
    url(r'^orders/query/$', views.order_query, name='order_query'),
    url(r'^orders/shoppinglist/$', views.order_shoplist, name='order_shoplist'),
    url(r'^orders/purchase/$', views.order_purchase, name='order_purchase'),
    url(r'^orders/save/$', views.order_save, name='order_save'),
    url(r'^orders/del/$', views.order_del, name='order_del'),
    url(r'^orders/delete/(?P<order_id>\w+)$', views.order_cancel, name='order_cancel'),
    url(r'^orders/(.*).json$',views.orderjson_resource),
    url(r'^foods/del/$', views.food_del, name='food_del'),
    url(r'^foods/srch/$', views.food_srch, name='food_srch'),
    url(r'^catalog/del/$', views.cata_del, name='cata_del'),
    url(r'^catalog/save/$', views.cata_save, name='cata_save'),
    url(r'^users/save/$', views.user_save, name='user_save'),
    url(r'^users/del/$', views.user_del, name='user_del'),
    url(r'^users/query/$', views.user_query, name='user_query'),
    url(r'^customers/edit/(?P<open_id>\w+)$', views.cedit, name='customer_edit'),
    url(r'^admin/(.*).jpg$',views.jpg_resource),
    url(r'^admin/exit$', views.mylogout, name='exit'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^addr/$', views.add_addr, name='addr'),
    url(r'^zan/$', views.zan_add, name='zan_add'),
    url(r'^dltime/add/$', views.add_dltime, name='dltime_add'),
    url(r'^dltime/save/$', views.save_dltime, name='dltime_save'),
    url(r'^dltime/del/$', views.del_dltime, name='dltime_del'),
    url(r'^dladdr/save/$', views.dladdr_save, name='dladdr_save'),
    url(r'^dladdr/del/$', views.dladdr_del, name='dladdr_del'),
    url(r'^otherset/save/$', views.save_otherset, name='otherset_save'),
    url(r'^ingredit/save/$', views.ingredit_save, name='ingredit_save'),
    url(r'^ingredit/delete/$', views.ingredit_del, name='ingredit_del'),
    url(r'^ingredit/query/$', views.ingredit_query, name='ingredit_query'),
    url(r'^alipay$', views.alipay_rsp, name='alipay'),
    url(r'^$', views.index, name='index'),
    url(r'^(.*).js$',views.js_resource),
    url(r'^(.*).css$',views.css_resource),
    url(r'^(.*).gif$',views.gif_resource),
    url(r'^(.*).png$',views.png_resource),
    url(r'^(.*).jpg$',views.jpg_resource),
    url(r'^(.*).json$',views.json_resource),
    url(r'^skin/(.*).htm$',views.htm_resource),
    url(r'^skin/tiny_mce/plugins/advimage/upload_image/', views.upload_image),
)
