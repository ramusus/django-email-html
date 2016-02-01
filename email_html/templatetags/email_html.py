from django import template
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup

try:
    unicode_type = unicode
except NameError:
    unicode_type = str

register = template.Library()

@register.filter
def html2text(value):
    """
    Pipes given HTML string into the text browser W3M, which renders it.
    Rendered text is grabbed from STDOUT and returned.
    """
    try:
        cmd = "w3m -dump -T text/html -O utf-8"
        proc = Popen(cmd, shell = True, stdin = PIPE, stdout = PIPE)
        return proc.communicate(str(value))[0]
    except OSError:
        # something bad happened, so just return the input
        return value

@register.filter
def extract_urllinks(value, template='%(text)s (%(url)s)'):
    '''
    Extract urls from links and put it to brackets after links. Useful for generating plain version of email body from html
    '''
    html = BeautifulSoup(value)
    for link in html.findAll('a'):
        text = ''.join(map(unicode_type, link.contents)).strip()
        if link.get('href') and link.get('href') != text:
            result = template % {
                'text': text,
                'url': link['href'].replace('\n',''),
            }
        elif text:
            result = text

        link.replaceWith(result)
    return html
