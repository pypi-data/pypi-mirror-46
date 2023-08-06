"""
Test models required for test cases
"""

from django.db import models

from django_tidyfields.fields import TidyCharField, TidyTextField

PERMISSIVE_TIDYFIELDS = {
    'allow_tags': ['b', 'em', 'i', 'strong', 'span', 'p', 'pagebreak'],
    'safe_attrs': ['class', 'style'],
    'style': False
}

XSS_TIDYFIELDS = {
    'allow_tags': [
        'b', 'em', 'i', 'strong', 'span', 'p', 'pagebreak', 'img', 'a', 'body', 'input', 'form', 'li', 'ul', 'style'
    ],
    'safe_attrs': ['class', 'style', 'src'],
    'style': False,
    'kill_tags': ['script']
}


class TestModel(models.Model):
    """
    A test model to test our TidyFields against.
    """

    test_id = models.IntegerField()
    title = TidyCharField(max_length=255)
    description = TidyTextField()
    byline = TidyCharField(field_args=PERMISSIVE_TIDYFIELDS, max_length=255)
    body = TidyTextField(field_args=PERMISSIVE_TIDYFIELDS)


class XSSModel(models.Model):
    """
    A test model to test our OWASP injections against.
    """

    test_id = models.IntegerField()
    title = TidyCharField(max_length=255)
    description = TidyTextField()
    byline = TidyCharField(field_args=XSS_TIDYFIELDS, max_length=255)
    body = TidyTextField(field_args=XSS_TIDYFIELDS)
