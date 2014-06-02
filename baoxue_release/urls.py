from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                       url(r'^$', 'release.views.home', name='home'),
                       url(r'^login/$', 'release.views.login', name='login'),
                       url(r'^logout/$', 'release.views.logout', name='logout'),
                       url(r'^upload/$', 'release.views.upload', name='upload'),
                       url(r'^branch_manage/(?P<id>.*?)$', 'release.views.branch_manage', name='branch_manage'),
                       url(r'^logo_manage/(?P<id>.*?)$', 'release.views.logo_manage', name='logo_manage'),
                       url(r'^logo_browse/(?P<id>.*?)$', 'release.views.logo_browse', name='logo_browse'),
                       url(r'^logo_delete/(?P<id>.*?)$', 'release.views.logo_delete', name='logo_delete'),
                       url(r'^branch_delete/(?P<id>.*?)$', 'release.views.branch_delete', name='branch_delete'),

                       url(r'^admin/', include(admin.site.urls)),
)
