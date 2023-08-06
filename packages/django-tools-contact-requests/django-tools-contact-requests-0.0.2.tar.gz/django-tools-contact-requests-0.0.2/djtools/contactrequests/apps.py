from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ContactRequestsConfig(AppConfig):
    name = 'djtools.contactrequests'
    label = 'djtools.contactrequests'
    verbose_name = 'Contact Requests'

    def ready(self):
        if not hasattr(settings, 'DJTOOLS_CONTACTREQUESTS_SITE_DOMAIN'):
            raise ImproperlyConfigured(
                "The DJTOOLS_CONTACTREQUESTS_SITE_DOMAIN setting must not be empty."
            )
        if not hasattr(settings, 'DJTOOLS_CONTACTREQUESTS_MAIL_FROM'):
            raise ImproperlyConfigured(
                "The DJTOOLS_CONTACTREQUESTS_MAIL_FROM setting must not be empty."
            )
        if not hasattr(settings, 'DJTOOLS_CONTACTREQUESTS_MAIL_TO'):
            raise ImproperlyConfigured(
                "The DJTOOLS_CONTACTREQUESTS_MAIL_TO setting must not be empty."
            )
