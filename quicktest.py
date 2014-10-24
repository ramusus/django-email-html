import os
import sys
import argparse
from django.conf import settings

'''
QuickDjangoTest module for testing in Travis CI https://travis-ci.org
Changes log:
 * 2014-10-24 updated for compatibility with Django 1.7
'''

class QuickDjangoTest(object):
    """
    A quick way to run the Django test suite without a fully-configured project.

    Example usage:

        >>> QuickDjangoTest('app1', 'app2')

    Based on a script published by Lukasz Dziedzia at:
    http://stackoverflow.com/questions/3841725/how-to-launch-tests-for-django-reusable-app
    """
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'email_html',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    )

    def __init__(self, *args, **kwargs):
        self.apps = args
        # Get the version of the test suite
        self.version = self.get_test_version()
        # Call the appropriate one
        if self.version == '1.7':
            self._tests_1_7()
        elif self.version == '1.2':
            self._tests_1_2()
        else:
            self._tests_old()

    def get_test_version(self):
        """
        Figure out which version of Django's test suite we have to play with.
        """
        from django import VERSION
        if VERSION[0] == 1 and VERSION[1] >= 7:
            return '1.7'
        elif VERSION[0] == 1 and VERSION[1] >= 2:
            return '1.2'
        else:
            return

    def _tests_old(self):
        """
        Fire up the Django test suite from before version 1.2
        """
        INSTALLED_APPS, settings_test = self.custom_settings()

        settings.configure(DEBUG = True,
            DATABASE_ENGINE = 'sqlite3',
            DATABASE_NAME = os.path.join(self.DIRNAME, 'database.db'),
            INSTALLED_APPS = self.INSTALLED_APPS + INSTALLED_APPS + self.apps,
            **settings_test
        )
        from django.test.simple import run_tests
        failures = run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

    def _tests_1_2(self):
        """
        Fire up the Django test suite developed for version 1.2 and up
        """
        INSTALLED_APPS, settings_test = self.custom_settings()

        settings.configure(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            INSTALLED_APPS = self.INSTALLED_APPS,# + INSTALLED_APPS + self.apps,
            **settings_test
        )

        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner().run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

    def _tests_1_7(self):
        """
        Fire up the Django test suite developed for version 1.7 and up
        """
        INSTALLED_APPS, settings_test = self.custom_settings()

        settings.configure(
            DEBUG = True,
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
                                  'django.middleware.csrf.CsrfViewMiddleware'),
            INSTALLED_APPS = self.INSTALLED_APPS,# + INSTALLED_APPS + self.apps,
            **settings_test
        )

        from django.test.simple import DjangoTestSuiteRunner
        import django
        django.setup()
        failures = DjangoTestSuiteRunner().run_tests(self.apps, verbosity=1)
        if failures:
            sys.exit(failures)

    def custom_settings(self):
        try:
            from settings_test import *
            settings_test = dict(locals())
            del settings_test['self']
            if 'INSTALLED_APPS' in settings_test:
                del settings_test['INSTALLED_APPS']
        except ImportError:
            settings_test = {}
            INSTALLED_APPS = []

        return INSTALLED_APPS, settings_test

if __name__ == '__main__':
    """
    What do when the user hits this file from the shell.

    Example usage:

        $ python quicktest.py app1 app2

    """
    parser = argparse.ArgumentParser(
        usage="[args]",
        description="Run Django tests on the provided applications."
    )
    parser.add_argument('apps', nargs='+', type=str)
    args = parser.parse_args()
    QuickDjangoTest(*args.apps)