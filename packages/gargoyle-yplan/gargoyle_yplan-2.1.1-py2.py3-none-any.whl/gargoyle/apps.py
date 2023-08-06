from __future__ import absolute_import, division, print_function, unicode_literals

from django.apps import AppConfig
from django.core import checks

from gargoyle.checks import check_switch_defaults


class GargoyleAppConfig(AppConfig):
    name = 'gargoyle'
    verbose_name = 'Gargoyle'

    def ready(self):
        checks.register(check_switch_defaults)
        self.module.autodiscover()
