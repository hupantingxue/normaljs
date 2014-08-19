from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qqcy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^microfront/home/register/', include('register.urls')),
    url(r'^microfront/', include('microfront.urls', namespace="microfront")),
    url(r'^micromall/', include('micromall.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^microfront/admin/', include('microfront.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
