from django.conf.urls import patterns, include, url
from django.contrib import admin
from djadmin import settings
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls), name='admin'),

    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
)

urlpatterns += patterns(
    '',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
