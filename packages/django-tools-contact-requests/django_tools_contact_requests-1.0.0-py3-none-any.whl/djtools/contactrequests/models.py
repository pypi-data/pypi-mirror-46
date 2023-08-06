from django.db import models
from django.utils.translation import gettext as _


class ContactRequest(models.Model):
    """
    This model will manage the requests from the contact form
    """

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email'))
    phone_number = models.CharField(_('phone number'), max_length=255)
    message = models.TextField(_('message'))
    contacted = models.BooleanField(_('contacted'), default=False)

    class Meta:
        verbose_name = _("Contact request")
        verbose_name_plural = _("Contact requests")

    def __str__(self):
        return self.name

    @property
    def contact_information(self):
        if self.email and self.phone_number:
            return _("{email} or {phone_number}").format(
                email=self.email,
                phone_number=self.phone_number
            )
        if self.email:
            return self.email
        return self.phone_number
