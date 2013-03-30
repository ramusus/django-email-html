# Django Email HTML

[![Build Status](https://travis-ci.org/ramusus/django-email-html.png?branch=master)](https://travis-ci.org/ramusus/django-email-html)

This application can be used for quickly switching all emails from plain-text to html. For using it you need to do 2 steps:

* add ``email_html`` to ``INSTALLED_APPS`` higher, then other third-party applications;
* change all email templates to new html version;

Application substitutes built-in ``send_mail`` function by new smart ``send_mail`` function.

build-in:

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None)

new:

    send_mail(subject, message, from_email=None, recipient_list=None, fail_silently=False, auth_user=None, auth_password=None, connection=None)

## Few new features:

* Message attribute using for html or plain-test message body. If it contains html, plain-text body will generated automatically based on html version;
* ``from_email`` attribute is not required. By default it will set from ``settings.DEFAULT_FROM_EMAIL``;
* Depending on ``settings.EMAIL_ADMIN_DUPLICATE`` all copies of email messages also sending to ``ADMIN`` emails (using bcc header);

New function can be used:

    send_mail(subj, html, recipient_list=emails)

## Requirements:

* BeautifulSoup
* w3m (for generating plain-text from html)

## Important notes:

* Place ``email_html`` application in ``INSTALLED_APPS`` before all other applications, which sending emails you need to make html based by default;
* Html body must contains <html> tag, otherwise function would think this is a plain-text body;