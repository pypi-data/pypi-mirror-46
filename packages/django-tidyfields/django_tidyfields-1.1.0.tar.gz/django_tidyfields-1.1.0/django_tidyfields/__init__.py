"""
Django TidyFields
"""
import re
from lxml.html.clean import Cleaner
from lxml.html import fromstring, tostring

__version__ = '1.1.0'

DEFAULT_APP_CONFIG = 'django_tidyfields.apps.DjangoTidyfieldsConfig'

NAME = "django_tidyfields"

TIDYFIELDS_DEFAULT = {
    'processing_instructions': True,
    'javascript': True,
    'comments': True,
    'style': True,
    'allow_tags': [],
    'remove_unknown_tags': False,
    'kill_tags': ['script', 'style'],
    'safe_attrs_only': True,
    'safe_attrs': [],
    'add_nofollow': True,
    'scripts': True,
    'inline_style': None,
    'links': True,
    'meta': True,
    'page_structure': True,
    'embedded': True,
    'frames': True,
    'forms': True,
    'annoying_tags': True,
    'remove_tags': None,
    'host_whitelist': [],
    'whitelist_tags': {}
}

STRIP_TIDYWRAP_REGEX = re.compile(r'^<tidywrap>(.*)</tidywrap>$', flags=re.DOTALL)

def tidy_input(field_contents="", **kwargs):
    """
    Take contents of field and arguments for `lxml.html.clean.Cleaner` and return sanitized string.

    :param field_contents: (string) string to be sanitized
    :param kwargs: (list) arguments for `Cleaner` class
    :return: (string) sanitized string
    """

    # Allow and wrap string in extra element so lxml doesn't feel the need to add a root element.
    kwargs['allow_tags'] = kwargs['allow_tags'] + ['tidywrap']
    tidied = tostring(
        Cleaner(**kwargs).clean_html(fromstring('<tidywrap>'+field_contents+'</tidywrap>')),
        encoding="unicode"
    )

    # Remove outer element added to prevent lxml adding unknown root element.
    tidied = STRIP_TIDYWRAP_REGEX.sub(r'\1', tidied)

    return tidied
