from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory
from django.views.generic import View

from adminplus.sites import AdminSitePlus


class AdminPlusTests(TestCase):
    def test_decorator(self):
        """register_view works as a decorator."""
        site = AdminSitePlus()

        @site.register_view(r'foo/bar')
        def foo_bar(request):
            return 'foo-bar'

        @site.register_view(r'foobar')
        class FooBar(View):
            def get(self, request):
                return 'foo-bar'

        urls = site.get_urls()
        assert any(u.resolve('foo/bar') for u in urls)
        assert any(u.resolve('foobar') for u in urls)

    def test_function(self):
        """register_view works as a function."""
        site = AdminSitePlus()

        def foo(request):
            return 'foo'
        site.register_view('foo', view=foo)

        class Foo(View):
            def get(self, request):
                return 'foo'
        site.register_view('bar', view=Foo)

        urls = site.get_urls()
        assert any(u.resolve('foo') for u in urls)
        assert any(u.resolve('bar') for u in urls)

    def test_path(self):
        """Setting the path works correctly."""
        site = AdminSitePlus()

        def foo(request):
            return 'foo'
        site.register_view('foo', view=foo)
        site.register_view('bar/baz', view=foo)
        site.register_view('baz-qux', view=foo)

        urls = site.get_urls()

        # the default admin contains a catchall view, so each will match 2
        foo_urls = [u for u in urls if u.resolve('foo')]
        self.assertEqual(2, len(foo_urls))
        bar_urls = [u for u in urls if u.resolve('bar/baz')]
        self.assertEqual(2, len(bar_urls))
        qux_urls = [u for u in urls if u.resolve('baz-qux')]
        self.assertEqual(2, len(qux_urls))

    def test_urlname(self):
        """Set URL pattern names correctly."""
        site = AdminSitePlus()

        @site.register_view('foo', urlname='foo')
        def foo(request):
            return 'foo'

        @site.register_view('bar')
        def bar(request):
            return 'bar'

        urls = site.get_urls()
        foo_urls = [u for u in urls if u.resolve('foo')]

        # the default admin contains a catchall view, so this will capture two
        self.assertEqual(2, len(foo_urls))
        self.assertEqual('foo', foo_urls[0].name)

        bar_urls = [u for u in urls if u.resolve('bar')]
        self.assertEqual(2, len(bar_urls))
        assert bar_urls[0].name is None

    def test_base_template(self):
        """Make sure extending the base template works everywhere."""
        result = render_to_string('adminplus/test/index.html')
        assert 'Ohai' in result

    def test_visibility(self):
        """Make sure visibility works."""
        site = AdminSitePlus()
        req_factory = RequestFactory()

        def always_visible(request):
            return 'i am here'
        site.register_view('always-visible', view=always_visible, visible=True)

        def always_hidden(request):
            return 'i am here, but not shown'
        site.register_view('always-hidden', view=always_visible, visible=False)

        cond = lambda req: req.user.pk == 1  # noqa: E731
        b = lambda s: s.encode('ascii') if hasattr(s, 'encode') else s  # noqa: #731

        @site.register_view(r'conditional-view', visible=cond)
        class ConditionallyVisible(View):
            def get(self, request):
                return 'hi there'

        urls = site.get_urls()
        assert any(u.resolve('always-visible') for u in urls)
        assert any(u.resolve('always-hidden') for u in urls)
        assert any(u.resolve('conditional-view') for u in urls)

        class MockUser(object):
            is_active = True
            is_staff = True

            def __init__(self, pk):
                self.pk = pk
                self.id = pk

        req_show = req_factory.get('/admin/')
        req_show.user = MockUser(1)
        result = site.index(req_show).render().content
        assert b('always-visible') in result
        assert b('always-hidden') not in result
        assert b('conditional-view') in result

        req_hide = req_factory.get('/admin/')
        req_hide.user = MockUser(2)
        result = site.index(req_hide).render().content
        assert b('always-visible') in result
        assert b('always-hidden') not in result
        assert b('conditional-view') not in result
