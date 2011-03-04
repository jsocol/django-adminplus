from django.contrib.admin.sites import AdminSite
from django.utils.text import capfirst


__version__ = '0.1'


class AdminSitePlus(AdminSite):
    """Extend AdminSite to allow registering custom admin views."""
    index_template = 'adminplus/index.html'  # That was easy.
    custom_views = []

    def register_view(self, path, view, name=None):
        """Add a custom admin view.

        * `path` is the path in the admin where the view will live, e.g.
            http://example.com/admin/somepath
        * `view` is any view function you can imagine.
        * `name` is an optional pretty name for the list of custom views. If
            empty, we'll guess based on view.__name__.
        """
        self.custom_views.append((path, view, name))

    def get_urls(self):
        """Add our custom views to the admin urlconf."""
        urls = super(KAdminSite, self).get_urls()
        from django.conf.urls.defaults import patterns, url, include
        for path, view, name in self.custom_views:
            urls += patterns('',
                url(r'^%s$' % path, self.admin_view(view)),
            )
        return urls

    def index(self, request, extra_context=None):
        """Make sure our list of custom views is on the index page."""
        if not extra_context:
            extra_context = {}
        custom_list = [(path, name if name else
                        capfirst(view.__name__)) for path, view, name in
                        self.custom_views]
        # Sort views alphabetically.
        custom_list.sort(lambda x: x[1])
        extra_context.update({
            'custom_list': custom_list
        })
        return super(KAdminSite, self).index(request, extra_context)
