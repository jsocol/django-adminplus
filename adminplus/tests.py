from django.test import TestCase

from adminplus.sites import AdminSitePlus


class AdminPlusTests(TestCase):
    def test_decorator(self):
        """register_view works as a decorator."""
        site = AdminSitePlus()

        @site.register_view(r'foo/bar')
        def foo_bar(request):
            return 'foo-bar'

        urls = site.get_urls()
        assert any(u.resolve('foo/bar') for u in urls)

    def test_function(self):
        """register_view works as a function."""
        site = AdminSitePlus()

        def foo(request):
            return 'foo'
        site.register_view('foo', view=foo)

        urls = site.get_urls()
        assert any(u.resolve('foo') for u in urls)

    def test_path(self):
        """Setting the path works correctly."""
        site = AdminSitePlus()

        def foo(request):
            return 'foo'
        site.register_view('foo', view=foo)
        site.register_view('bar/baz', view=foo)
        site.register_view('baz-qux', view=foo)

        urls = site.get_urls()

        foo_urls = [u for u in urls if u.resolve('foo')]
        self.assertEqual(1, len(foo_urls))
        bar_urls = [u for u in urls if u.resolve('bar/baz')]
        self.assertEqual(1, len(bar_urls))
        qux_urls = [u for u in urls if u.resolve('baz-qux')]
        self.assertEqual(1, len(qux_urls))

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
        self.assertEqual(1, len(foo_urls))
        self.assertEqual('foo', foo_urls[0].name)

        bar_urls = [u for u in urls if u.resolve('bar')]
        self.assertEqual(1, len(bar_urls))
        assert bar_urls[0].name is None
