from setuptools import setup, find_packages

setup(
    name='django-email-html',
    version=__import__('email_html').__version__,
    description='Application for switching from Django plain-text emails to html emails with 2 bodies: html and plain-text, generated automatically from html',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-email-html',
    download_url='http://pypi.python.org/pypi/django-email-html',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=[
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
