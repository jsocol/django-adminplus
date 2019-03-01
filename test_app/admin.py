from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin


@admin.site.register_view('mypath', name='A Fancy View')
def myview(request):
    return 'This is a view'
