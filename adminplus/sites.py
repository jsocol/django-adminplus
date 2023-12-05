from collections import namedtuple
import inspect
from typing import Any, Callable, NewType, Sequence, Union

from django.contrib.admin.sites import AdminSite
from django.urls import URLPattern, URLResolver, path
from django.utils.text import capfirst
from django.views.generic import View


_FuncT = NewType('_FuncT', Callable[..., Any])

AdminView = namedtuple('AdminView',
                       ['path', 'view', 'name', 'urlname', 'visible'])


def is_class_based_view(view):
    return inspect.isclass(view) and issubclass(view, View)


class AdminPlusMixin(object):
    """Mixin for AdminSite to allow registering custom admin views."""

    index_template = 'adminplus/index.html'  # That was easy.

    def __init__(self, *args, **kwargs):
        self.custom_views: list[AdminView] = []
        return super().__init__(*args, **kwargs)

    def register_view(self, slug, name=None, urlname=None, visible=True,
                      view=None) -> Union[None, Callable[[_FuncT], _FuncT]]:
        """Add a custom admin view. Can be used as a function or a decorator.

        * `path` is the path in the admin where the view will live, e.g.
            http://example.com/admin/somepath
        * `name` is an optional pretty name for the list of custom views. If
            empty, we'll guess based on view.__name__.
        * `urlname` is an optional parameter to be able to call the view with a
            redirect() or reverse()
        * `visible` is a boolean or predicate returning one, to set if
            the custom view should be visible in the admin dashboard or not.
        * `view` is any view function you can imagine.
        """
        def decorator(fn: _FuncT):
            if is_class_based_view(fn):
                fn = fn.as_view()
            self.custom_views.append(
                    AdminView(slug, fn, name, urlname, visible))
            return fn
        if view is not None:
            decorator(view)
            return
        return decorator

    def get_urls(self) -> Sequence[Union[URLPattern, URLResolver]]:
        """Add our custom views to the admin urlconf."""
        urls: list[Union[URLPattern, URLResolver]] = super().get_urls()
        for av in self.custom_views:
            urls.insert(
                0, path(av.path, self.admin_view(av.view), name=av.urlname))
        return urls

    def index(self, request, extra_context=None):
        """Make sure our list of custom views is on the index page."""
        if not extra_context:
            extra_context = {}
        custom_list = []
        for slug, view, name, _, visible in self.custom_views:
            if callable(visible):
                visible = visible(request)
            if visible:
                if name:
                    custom_list.append((slug, name))
                else:
                    custom_list.append((slug, capfirst(view.__name__)))

        # Sort views alphabetically.
        custom_list.sort(key=lambda x: x[1])
        extra_context.update({
            'custom_list': custom_list
        })
        return super().index(request, extra_context)


class AdminSitePlus(AdminPlusMixin, AdminSite):
    """A Django AdminSite with the AdminPlusMixin to allow registering custom
    views not connected to models."""
