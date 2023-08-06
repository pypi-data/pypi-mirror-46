# Django Tools Contact Requests

Simple Django app to manage contact requests

## Installation

1. Install with pip install `django-tools-contact-requests`.

2. Add `djtools.contactrequests` to your INSTALLED_APPS setting like this:
```
INSTALLED_APPS = [
    ...
    'djtools.contactrequests',
]
```

3. Add your contact information in your project settings:
```
DJTOOLS_CONTACTREQUESTS_SITE_DOMAIN = "www.example.com"
DJTOOLS_CONTACTREQUESTS_MAIL_FROM = "no-reply@example.com"
DJTOOLS_CONTACTREQUESTS_MAIL_TO = ["admin@example.com"]
```

4. It has a dependency over `django-recaptcha`. Follow their instructions as well:
[Django ReCaptcha](https://github.com/praekelt/django-recaptcha).


5. You can use the `ContactRequestView` like this:
```
from djtools.contactrequests.views import ContactRequestView


urlpatterns = [
    path('contact/', ContactRequestView.as_view(), name='contact'),
]
```

6. Run `python manage.py migrate` to create the contact models.
