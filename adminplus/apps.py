from django.contrib.admin.apps import AdminConfig


class AdminPlusConfig(AdminConfig):
    default_site = 'adminplus.sites.AdminSitePlus'
