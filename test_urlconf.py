try:  # Django 2+
    from django.urls import re_path as url, include
except ImportError:
    from django.conf.urls import url, include
from django.contrib import admin

from adminplus.sites import AdminSitePlus


admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
