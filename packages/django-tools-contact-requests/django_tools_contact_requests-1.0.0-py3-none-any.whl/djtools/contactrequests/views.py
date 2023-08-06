from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from . import forms, services


class ContactRequestView(FormView):
    form_class = forms.ContactRequestForm
    template_name = 'djtools/contactrequests/contactrequest_form.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        """
        Displays a success message when the form is submitted correctly
        """

        services.create_contact_request(**form.cleaned_data)
        messages.success(self.request, _("Your request has been submitted."))
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Displays an error message when the form is submitted with errors
        """

        messages.error(self.request, _("Please, check the form errors."))
        return super().form_invalid(form)
