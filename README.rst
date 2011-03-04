================
Django AdminPlus
================

**AdminPlus** aims to be the smallest possible extension to the excellent
Django admin component that lets you add admin views that are not tied to
models.

There are packages out there, like `Nexus <https://github.com/disqus/nexus>`_
and `django-admin-tools <http://pypi.python.org/pypi/django-admin-tools>`_ that
replace the entire admin. Nexus supports adding completely new "modules" (the
Django model admin is a default module) but there seems to be a lot of boiler
plate code to do it. django-admin-tools does not, as far as I can tell, support
adding custom pages.

All AdminPlus does is allow you to add simple custom views (well, they can be
as complex as you like!) without mucking about with hijacking URLs, and
providing links to them right in the admin index.


Installing AdminPlus
====================

Grab AdminPlus from `github <https://github.com/jsocol/django-adminplus>`_ with
pip::

    pip install -e git://github.com/jsocol/django-adminplus

To use AdminPlus in your Django project, you'll need to replace
``django.contrib.admin.site``, which is an instance of
``django.contrib.admin.sites.AdminSite``. I recommend doing this in ``urls.py``
right before calling ``admin.autodiscover()``::

    # urls.py
    from django.contrib import admin
    from adminplus import AdminSitePlus

    admin.site = AdminSitePlus()
    admin.autodiscover()

    urlpatterns = patterns('',
        # ...
        # Include the admin URL conf as normal.
        (r'^admin', include(admin.site.urls)),
        # ...
    )

Congratulations! You're now using AdminPlus.


Using AdminPlus
===============

So now that you've installed AdminPlus, you'll want to use it. AdminPlus is
100% compatible with the built in admin module, so if you've been using that,
you shouldn't have to change anything.

AdminPlus offers a new function, ``admin.site.register_view``, to attach
arbitrary views to the admin::

    # someapp/admin.py
    # Assuming you've replaced django.contrib.admin.site as above.
    from django.contrib import admin

    def my_view(request, *args, **kwargs):
        pass
    admin.site.register_view('somepath', my_view)

    # And of course, this still works:
    from someapp.models import MyModel
    admin.site.register(MyModel)

Now ``my_view`` will be accessible at ``admin/somepath`` and there will be a
link to it in the *Custom Views* section of the admin index.

``register_view`` takes a 3rd, optional argument: a friendly name for display
in the list of custom views. For example::

    def my_view(request):
        """Does something fancy!"""
    admin.site.register_view('somepath', my_view, 'My Fancy Admin View!')

All registered views are wrapped in ``admin.site.admin_view``.
