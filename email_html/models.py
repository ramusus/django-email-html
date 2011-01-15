# substitute send_mail function.
from django.conf import settings
from mail import send_mail as send_html_mail

from django.core import mail
mail.send_mail = send_html_mail

if 'mailer' in settings.INSTALLED_APPS:
    import mailer
    mailer.send_mail = send_html_mail