from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.core.checks import Warning


def check_switch_defaults(app_configs, **kwargs):
    errors = []
    if hasattr(settings, 'GARGOYLE_SWITCH_DEFAULTS'):
        for key, switch_defaults in settings.GARGOYLE_SWITCH_DEFAULTS.items():
            if 'is_active' in switch_defaults and 'initial_status' in switch_defaults:
                errors.append(Warning(
                    '"is_active" will take precedence over "initial_status" in GARGOYLE_SWITCH_DEFAULTS.',
                    hint="settings.GARGOYLE_SWITCH_DEFAULTS['{}']".format(key),
                    id='gargoyle.001',
                ))
    return errors
