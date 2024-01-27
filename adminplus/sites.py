import inspect
from collections import namedtuple
from typing import Any, Callable, NewType, Sequence, Union

from django.contrib.admin.sites import AdminSite
from django.urls import URLPattern, URLResolver, path, reverse
from django.utils.text import capfirst
from django.views.generic import View

_FuncT = NewType("_FuncT", Callable[..., Any])

AdminView = namedtuple(
    "AdminView", ["path", "view", "name", "urlname", "visible"]
)


def is_class_based_view(view):
    return inspect.isclass(view) and issubclass(view, View)


class AdminPlusMixin(object):
    """Mixin for AdminSite to allow registering custom admin views."""

    custom_views_title = "Custom Views"

    def __init__(self, *args, **kwargs):
        self.custom_views: list[AdminView] = []
        super().__init__(*args, **kwargs)

    def register_view(
        self, slug, name=None, urlname=None, visible=True, view=None
    ) -> Union[None, Callable[[_FuncT], _FuncT]]:
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
                AdminView(slug, fn, name, urlname, visible)
            )
            return fn

        if view is not None:
            decorator(view)
            return
        return decorator

    def get_urls(self) -> Sequence[Union[URLPattern, URLResolver]]:
        """Add our custom views to the admin urlconf."""
        urls: list[Union[URLPattern, URLResolver]] = super().get_urls()
        urls.insert(
            0,
            path(
                "adminplus/",
                self.admin_view(self.app_index),
                kwargs={"app_label": "adminplus"},
                name="app_list_adminplus",
            ),
        )
        for av in self.custom_views:
            urls.insert(
                0, path(av.path, self.admin_view(av.view), name=av.urlname)
            )
        return urls

    def get_app_list(self, request, app_label=None):
        # Django 3.2 don't have app_label parameter
        kwargs = {}
        sig = inspect.signature(super(AdminPlusMixin, self).get_app_list)
        for p in sig.parameters.values():
            if p.name == "app_label":
                kwargs["app_label"] = app_label
        app_list = super().get_app_list(request, **kwargs)
        if app_label is None or app_label == "adminplus":
            root_url = reverse("admin:index")
            custom_list = []
            for av in self.custom_views:
                visible = av.visible
                if callable(visible):
                    visible = visible(request)
                if visible:
                    name = av.name
                    if not name:
                        name = capfirst(av.view.__name__)
                    custom_list.append(
                        {
                            "model": None,
                            "name": name,
                            "object_name": av.view.__name__,
                            "admin_url": "%s%s" % (root_url, av.path),
                            "add_url": "",
                            "view_only": True,
                            "perms": {
                                "add": False,
                                "change": False,
                                "delete": False,
                                "view": True,
                            },
                        }
                    )

            # Sort views alphabetically.
            custom_list.sort(key=lambda x: x["name"])

            app_list.append(
                {
                    "name": self.custom_views_title,
                    "app_label": "adminplus",
                    "app_url": reverse("admin:app_list_adminplus"),
                    "has_module_perms": True,
                    "models": custom_list,
                }
            )
        return app_list


class AdminSitePlus(AdminPlusMixin, AdminSite):
    """A Django AdminSite with the AdminPlusMixin to allow registering custom
    views not connected to models."""
