from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from templatetags.email_html import html2text, extract_urllinks
import re

def send_mail(subject, message, from_email=None, recipient_list=None,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    '''
    Replacement for monkey-patching Django's send_mail function for sending html email by default
    '''
    if recipient_list is None:
        raise ValueError('You must specified recipient_list attribute')

    admins = [a[1] for a in settings.ADMINS] if getattr(settings, 'EMAIL_ADMIN_DUPLICATE', False) else []
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    subject = settings.EMAIL_SUBJECT_PREFIX + subject.replace('\n', '')

    if message.find('<html>') != -1:
        message_plaintext = html2text(extract_urllinks(message))
        message_plaintext = re.sub(r'http://\n', 'http://', message_plaintext)
        if 'mailer' in settings.INSTALLED_APPS:
            from mailer import send_html_mail
            return send_html_mail(subject=subject, message=message_plaintext, message_html=message,
                                   from_email=from_email, recipient_list=recipient_list, bcc=admins,
                                   fail_silently=fail_silently, auth_user=auth_user,
                                   auth_password=auth_password)
        else:
            email = EmailMultiAlternatives(subject=subject, body=message_plaintext,
                                           from_email=from_email, to=recipient_list,
                                           bcc=admins, connection=connection)
            email.attach_alternative(message, "text/html")
            return email.send(fail_silently=fail_silently)

    else:
        email = EmailMessage(subject, message, from_email, recipient_list, admins)
        email.send(fail_silently=fail_silently)
