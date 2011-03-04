from django.contrib.admin.sites import AdminSite
from django.utils.text import capfirst


class AdminSitePlus(AdminSite):
    index_template = 'adminplus/index.html'
    custom_views = []

    def register_view(self, path, view, name=None):
        self.custom_views.append((path, view, name))

    def get_urls(self):
        urls = super(KAdminSite, self).get_urls()
        from django.conf.urls.defaults import patterns, url, include
        for path, view, name in self.custom_views:
            urls += patterns('',
                url(r'^%s$' % path, self.admin_view(view)),
            )
        return urls

    def index(self, request, extra_context=None):
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
