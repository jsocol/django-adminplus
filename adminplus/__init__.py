from __future__ import absolute_import

try:
    from .sites import AdminSitePlus

    site = AdminSitePlus()
except ImportError:
    pass


VERSION = (0, 2, 'dev')
__version__ = '.'.join(map(str, VERSION))
__all__ = ['AdminSitePlus', 'site']
