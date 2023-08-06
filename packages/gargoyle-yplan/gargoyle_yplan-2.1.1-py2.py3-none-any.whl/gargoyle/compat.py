from __future__ import absolute_import, division, print_function, unicode_literals

# Django 2.0

try:
    from django.urls import reverse  # noqa pragma: no cover
except ImportError:
    from django.core.urlresolvers import reverse  # noqa pragma: no cover
