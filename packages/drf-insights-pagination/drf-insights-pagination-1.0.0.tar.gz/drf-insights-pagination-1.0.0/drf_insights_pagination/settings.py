"""This module provides the `insights_pagination_settings` object."""

from django.conf import settings
from django.core.signals import setting_changed

INSIGHTS_PAGINATION_SETTINGS_PREFIX = "INSIGHTS_PAGINATION_"

DEFAULTS = {"APP_PATH": ""}


class InsightsPaginationSettings(object):
    """Settings object that allows insights pagination settings to be accessed."""

    def __init__(self, user_settings=settings, defaults=DEFAULTS):
        """Initialize the object."""
        self.defaults = defaults
        self.user_settings = user_settings

    def __getattr__(self, attr):
        """Get object attribute."""
        if attr not in self.defaults:
            raise AttributeError("Invalid Insights Pagination setting: '%s'" % attr)

        value = getattr(
            self.user_settings,
            INSIGHTS_PAGINATION_SETTINGS_PREFIX + attr,
            self.defaults[attr],
        )

        # Cache the result
        setattr(self, attr, value)
        return value


insights_pagination_settings = InsightsPaginationSettings()


def reload_insights_pagination_settings(*args, **kwargs):
    """Reload settings."""
    django_setting = kwargs["setting"]
    setting = django_setting.replace(INSIGHTS_PAGINATION_SETTINGS_PREFIX, "")
    value = kwargs["value"]
    if setting in DEFAULTS.keys():
        if value is not None:
            setattr(insights_pagination_settings, setting, value)
        elif hasattr(insights_pagination_settings, setting):
            delattr(insights_pagination_settings, setting)


setting_changed.connect(reload_insights_pagination_settings)
