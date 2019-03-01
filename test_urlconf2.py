from django.contrib import admin
from django.urls import path

from adminplus.sites import AdminSitePlus


admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
]
