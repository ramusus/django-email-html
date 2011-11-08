#!/usr/bin/env python

METADATA = dict(
    name='django-email-html',
    version='0.1',
    author='ramusus',
    description='Application for switching from Django plain-text emails to html emails with 2 bodies: html and plain-text, generated automatically from html',
    long_description=open('README').read(),
    url='http://github.com/ramusus/django-email-html',
    install_requires=[
        'beautifulsoup',
    ],
)

if __name__ == '__main__':
    try:
        import setuptools
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)
