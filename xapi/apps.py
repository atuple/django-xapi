from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _
import xapi


class XApiConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'xapi'
    verbose_name = _("Administration")

    def ready(self):
        self.module.autodiscover()
        setattr(xapi, 'site', xapi.site)
