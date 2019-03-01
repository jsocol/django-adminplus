import django
from django.conf.urls import url, include
from django.contrib import admin

from adminplus.sites import AdminSitePlus


if django.version < (2, 1):
    admin.site = AdminSitePlus()
    admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
