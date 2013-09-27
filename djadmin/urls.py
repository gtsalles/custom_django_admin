from django.conf.urls import patterns, include, url
from django.contrib import admin
from djadmin import settings
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls), name='admin'),
)

urlpatterns += patterns(
    '',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
