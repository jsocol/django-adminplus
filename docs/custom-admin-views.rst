===========================
Creating Custom Admin Views
===========================

Any view can be used as a custom admin view in AdminPlus. All the normal
rules apply: accept a request and possibly other parameters, return a
response, and you're good.

Making views look like the rest of the admin is pretty straight-forward,
too.


Extending the Admin Templates
=============================

AdminPlus contains an base template you can easily extend. It includes
the breadcrumb boilerplate. You can also extend ``admin/base_site.html``
directly.

Your view should pass a ``title`` value to the template to make things
pretty.

Here's an example template::

    {# myapp/admin/myview.html #}
    {% extends 'adminplus/base.html' %}

    {% block content %}
        {# Do what you gotta do. #}
    {% endblock %}

That's pretty much it! Now here's how you use it::

    # myapp/admin.py
    # Using AdminPlus
    from django.contrib import admin
    from django.shortcuts import render_to_response
    from django.template import RequestContext

    def myview(request):
        # Fanciness.
        return render_to_response('myapp/admin/myview.html',
                                  {'title': 'My View'},
                                  RequestContext(request, {}))
    admin.site.register_view('mypath', myview, 'My View')

Or, you can use it as a decorator::

    from django.contrib import admin

    @admin.site.register_view
    def myview(request):
        # Fancy goes here.
        return render_to_response(...)

Voila! Instant custom admin page that looks great.
