from django.conf.urls import patterns, url, include
from django.contrib import admin

from adminplus.sites import AdminSitePlus


admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
