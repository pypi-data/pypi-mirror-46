from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .models import ContactRequest


def _send_mail(contact_request):
    """
    Given a contact request instance sends an email to the web admin with the
    notification about its creation.
    Retruns the amount of sent emails.
    """

    site_domain = settings.DJTOOLS_CONTACTREQUESTS_SITE_DOMAIN
    message = render_to_string(
        'djtools/contactrequests/contactrequest_email.txt',
        {
            'object': contact_request,
            'DJTOOLS_CONTACTREQUESTS_SITE_DOMAIN': site_domain
        }
    )

    return send_mail(
        subject=_(f"You have a contact request from {site_domain}"),
        message=message,
        from_email=settings.DJTOOLS_CONTACTREQUESTS_MAIL_FROM,
        recipient_list=settings.DJTOOLS_CONTACTREQUESTS_MAIL_TO,
        fail_silently=False,
    )


def create_contact_request(name, email, phone_number, message, captcha=None):
    """
    Creates a new instance of ContactRequest and sends a notification email.
    captcha argument can be ignored
    """

    contact_request = ContactRequest.objects.create(
        name=name,
        email=email,
        phone_number=phone_number,
        message=message
    )
    amount_sent_emails = _send_mail(contact_request)
    return contact_request, amount_sent_emails
