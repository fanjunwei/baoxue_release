from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'release.views.home', name='home'),
                       url(r'^login/$','release.views.login',name='login' ),
                       url(r'^logout/$','release.views.logout',name='logout' ),
                       url(r'^upload/$','release.views.upload',name='upload' ),
                       url(r'^branch_manage/$','release.views.branch_manage',name='branch_manage' ),

                       url(r'^admin/', include(admin.site.urls)),
)
