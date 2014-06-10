# substitute send_mail function.
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from .mail import send_mail as send_html_mail

mail.send_mail = send_html_mail

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#referencing-the-user-model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    pass

def email_user(self, subject, message, from_email=None):
     """
     Sends an email to this User.
     """
     send_html_mail(subject, message, from_email, [self.email])

User.email_user = email_user

if 'mailer' in settings.INSTALLED_APPS:
    import mailer
    mailer.send_mail = send_html_mail