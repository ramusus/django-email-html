# substitute send_mail function.
from django.conf import settings
from django.core import mail
from .mail import send_mail as send_html_mail
import django

mail.send_mail = send_html_mail

if django.VERSION[0] == 1 and django.VERSION[1] >= 7:
    from django.core.exceptions import AppRegistryNotReady
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # TODO: impossible to user custom user model in Django 1.7 due to exception
        # django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
    except AppRegistryNotReady:
        from django.contrib.auth.models import User
else:
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#referencing-the-user-model
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    except ImportError:
        from django.contrib.auth.models import User


def email_user(self, subject, message, from_email=None, **kwargs):
     """
     Sends an email to this User.
     """
     send_html_mail(subject, message, from_email, [self.email], **kwargs)

User.email_user = email_user

if 'mailer' in settings.INSTALLED_APPS:
    import mailer
    mailer.send_mail = send_html_mail