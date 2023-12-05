from django.contrib import admin
from django.urls import re_path, include

from adminplus.sites import AdminSitePlus


admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', include((admin.site.get_urls(), 'admin'), namespace='admin')),
]
