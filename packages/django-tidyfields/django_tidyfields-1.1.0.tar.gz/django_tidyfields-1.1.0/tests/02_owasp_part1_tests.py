"""
Test OWASP attacks against parser.
"""
import pytest
from testapp.models import XSSModel


TEST_OWASP_XSS_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_BASIC_XSS = {
    'test_id': 1,
    'title': 'Test<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'description': 'Testing<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_js_is_removed():
    """
    Verify that basic XSS scripts are removed.
    """
    XSSModel.objects.create(**TEST_OWASP_BASIC_XSS)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_CLEAN['body']


TEST_OWASP_XSS_LOCATOR_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>javascript:/*--&gt;'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_LOCATOR = {
    'test_id': 1,
    'title': 'Test<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'description': 'Testing<SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT SRC=http://xss.rocks/xss.js></SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>javascript:/*--></title></style></textarea></script>'
            '</xmp><svg/onload=\'+/"/+/onmouseover=1/+/[*/[]/+alert(1)//\'>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_locator_is_removed():
    """
    Verify that XSS Locator attack is removed.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_LOCATOR)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_LOCATOR_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_LOCATOR_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_LOCATOR_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_LOCATOR_CLEAN['body']


TEST_OWASP_XSS_IMG_JS_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_JS = {
    'test_id': 1,
    'title': 'Test<IMG SRC="javascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="javascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="javascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="javascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_js_removed():
    """
    Verify that basic XSS <img src=""> attack is removed.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_JS)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_JS_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_JS_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_JS_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_JS_CLEAN['body']


TEST_OWASP_XSS_IMG_JS_NO_QUOTES_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_JS_NO_QUOTES = {
    'test_id': 1,
    'title': 'Test<IMG SRC=javascript:alert(\'XSS\')>',
    'description': 'Testing<IMG SRC=javascript:alert(\'XSS\')>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=javascript:alert(\'XSS\')>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=javascript:alert(\'XSS\')>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_js_no_quotes_removed():
    """
    Verify that basic XSS <img src=""> attack is removed when no quotes are provided.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_JS_NO_QUOTES)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_JS_NO_QUOTES_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_JS_NO_QUOTES_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_JS_NO_QUOTES_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_JS_NO_QUOTES_CLEAN['body']


TEST_OWASP_XSS_IMG_JS_CASE_MATCH_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_JS_CASE_MATCH = {
    'test_id': 1,
    'title': 'Test<IMG SRC=JaVaScRiPt:alert(\'XSS\')>',
    'description': 'Testing<IMG SRC=JaVaScRiPt:alert(\'XSS\')>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=JaVaScRiPt:alert(\'XSS\')>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=JaVaScRiPt:alert(\'XSS\')>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_js_case_match_removed():
    """
    Verify that cased XSS <img src=""> attack is removed.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_JS_CASE_MATCH)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_JS_CASE_MATCH_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_JS_CASE_MATCH_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_JS_CASE_MATCH_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_JS_CASE_MATCH_CLEAN['body']


TEST_OWASP_XSS_IMG_JS_ENTITIES_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_JS_ENTITIES = {
    'test_id': 1,
    'title': 'Test<IMG SRC=javascript:alert(&quot;XSS&quot;)>',
    'description': 'Testing<IMG SRC=javascript:alert(&quot;XSS&quot;)>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=javascript:alert(&quot;XSS&quot;)>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=javascript:alert(&quot;XSS&quot;)>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_js_entities_removed():
    """
    Verify that XSS <img src=""> attack is removed when html encoded.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_JS_ENTITIES)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_JS_ENTITIES_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_JS_ENTITIES_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_JS_ENTITIES_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_JS_ENTITIES_CLEAN['body']


TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT = {
    'test_id': 1,
    'title': 'Test<IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>',
    'description': 'Testing<IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=`javascript:alert("RSnake says, \'XSS\'")`>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_js_grave_accent_removed():
    """
    Verify that XSS <img src=""> attack is removed when grave accents surround it.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_JS_GRAVE_ACCENT_CLEAN['body']


TEST_OWASP_XSS_A_MALFORMED_CLEAN = {
    'test_id': 1,
    'title': 'Testxxs link',
    'description': 'Testingxxs link',
    'byline': '<i>A very basic model for OWASP tests</i><a>xxs link</a>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><a>xxs link</a>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_A_MALFORMED = {
    'test_id': 1,
    'title': 'Test<a onmouseover="alert(document.cookie)">xxs link</a>',
    'description': 'Testing<a onmouseover="alert(document.cookie)">xxs link</a>',
    'byline': '<i>A very basic model for OWASP tests</i><a onmouseover="alert(document.cookie)">xxs link</a>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><a onmouseover="alert(document.cookie)">xxs link</a>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_a_malformed_removed():
    """
    Verify that XSS malformed <a> attack is removed.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_A_MALFORMED)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_A_MALFORMED_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_A_MALFORMED_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_A_MALFORMED_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_A_MALFORMED_CLEAN['body']


TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES_CLEAN = {
    'test_id': 1,
    'title': 'Testxxs link',
    'description': 'Testingxxs link',
    'byline': '<i>A very basic model for OWASP tests</i><a>xxs link</a>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><a>xxs link</a>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES = {
    'test_id': 1,
    'title': 'Test<a onmouseover=alert(document.cookie)>xxs link</a>',
    'description': 'Testing<a onmouseover=alert(document.cookie)>xxs link</a>',
    'byline': '<i>A very basic model for OWASP tests</i><a onmouseover=alert(document.cookie)>xxs link</a>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><a onmouseover=alert(document.cookie)>xxs link</a>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_a_malformed_no_quotes_removed():
    """
    Verify that XSS malformed <a> attack is removed when no quotes are used.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_A_MALFORMED_NO_QUOTES_CLEAN['body']


TEST_OWASP_XSS_IMG_MALFORMED_CLEAN = {
    'test_id': 1,
    'title': 'Test"&gt;',
    'description': 'Testing"&gt;',
    'byline': '<i>A very basic model for OWASP tests</i><img>"&gt;',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img>"&gt;'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_MALFORMED = {
    'test_id': 1,
    'title': 'Test<IMG """><SCRIPT>alert("XSS")</SCRIPT>">',
    'description': 'Testing<IMG """><SCRIPT>alert("XSS")</SCRIPT>">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG """><SCRIPT>alert("XSS")</SCRIPT>">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG """><SCRIPT>alert("XSS")</SCRIPT>">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_malformed_removed():
    """
    Verify that XSS malformed <img> attack is removed.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_MALFORMED)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_MALFORMED_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_MALFORMED_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_MALFORMED_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_MALFORMED_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_CHARCODE_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_CHARCODE = {
    'test_id': 1,
    'title': 'Test<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>',
    'description': 'Testing<IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=javascript:alert(String.fromCharCode(88,83,83))>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_charcode_removed():
    """
    Verify that XSS <img src=""> attack is removed when using charcodes.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_CHARCODE)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_CHARCODE_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_CHARCODE_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_CHARCODE_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_CHARCODE_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_COMMENT_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="#">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="#">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_COMMENT = {
    'test_id': 1,
    'title': 'Test<IMG SRC=# onmouseover="alert(\'xxs\')">',
    'description': 'Testing<IMG SRC=# onmouseover="alert(\'xxs\')">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=# onmouseover="alert(\'xxs\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=# onmouseover="alert(\'xxs\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_comment_removed():
    """
    Verify that XSS <img src=""> attack is removed when SRC is a Hash.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_COMMENT)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_COMMENT_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_COMMENT_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_COMMENT_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_COMMENT_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_EMPTY_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="onmouseover=%22alert(\'xxs\')%22">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="onmouseover=%22alert(\'xxs\')%22">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_EMPTY = {
    'test_id': 1,
    'title': 'Test<IMG SRC= onmouseover="alert(\'xxs\')">',
    'description': 'Testing<IMG SRC= onmouseover="alert(\'xxs\')">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC= onmouseover="alert(\'xxs\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC= onmouseover="alert(\'xxs\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_empty_removed():
    """
    Verify that XSS <img src=""> attack is removed when SRC is empty.
    NOTE: This one leaves <img src="onmouseover=%22alert('xxs')%22"> as a result, however testing shows the
    remaining code is ineffective.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMPTY)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMPTY_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMPTY_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMPTY_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMPTY_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_ABSENT_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_ABSENT = {
    'test_id': 1,
    'title': 'Test<IMG onmouseover="alert(\'xxs\')">',
    'description': 'Testing<IMG onmouseover="alert(\'xxs\')">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG onmouseover="alert(\'xxs\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG onmouseover="alert(\'xxs\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_absent_removed():
    """
    Verify that XSS <img src=""> attack is removed when SRC is absent.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_ABSENT)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_ABSENT_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_ABSENT_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_ABSENT_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_ABSENT_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_SLASH_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A model for OWASP tests</i><img src="/">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="/">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_SLASH = {
    'test_id': 1,
    'title': 'Test<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>',
    'description': 'Testing<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>',
    'byline': '<i>A model for OWASP tests</i><IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_slash_removed():
    """
    Verify that XSS <img src=""> attack is removed when using "/" in SRC.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_SLASH)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_SLASH_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_SLASH_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_SLASH_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_SLASH_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A model for OWASP tests</i><img src="x">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="x">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR = {
    'test_id': 1,
    'title': 'Test<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105'
             '&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000'
             '088&#0000083&#0000083&#0000039&#0000041">',
    'description': 'Testing<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114'
                   '&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040'
                   '&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">',
    'byline': '<i>A model for OWASP tests</i><img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115'
              '&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#000'
              '0116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099'
            '&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116'
            '&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_encoded_onerror_removed():
    """
    Verify that XSS <img src=""> attack is removed when using HTML chars in an onerror.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_ENCODED_ONERROR_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS = {
    'test_id': 1,
    'title': 'Test<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;'
             '&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>',
    'description': 'Testing<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;'
                   '&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>',
    'byline': '<i>A model for OWASP tests</i><IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;'
              '&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;'
            '&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_encoded_html_chars_removed():
    """
    Verify that XSS <img src=""> attack is removed when using HTML chars.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS = {
    'test_id': 1,
    'title': 'Test<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112'
             '&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088'
             '&#0000083&#0000083&#0000039&#0000041>',
    'description': 'Testing<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105'
                   '&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040'
                   '&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>',
    'byline': '<i>A model for OWASP tests</i><IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099'
              '&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116'
              '&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114'
            '&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040'
            '&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_encoded_html_chars_no_semicolons_removed():
    """
    Verify that XSS <img src=""> attack is removed when using HTML chars without semicolons.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_CHARS_NO_SEMICOLONS_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX = {
    'test_id': 1,
    'title': 'Test<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72'
             '&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>',
    'description': 'Testing<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C'
                   '&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72'
              '&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61'
            '&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_encoded_html_hex_removed():
    """
    Verify that XSS <img src=""> attack is removed when using hex encoded HTML chars.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_ENCODED_HTML_HEX_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB = {
    'test_id': 1,
    'title': 'Test<IMG SRC="jav\tascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="jav\tascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="jav\tascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="jav\tascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_embedded_tab_removed():
    """
    Verify that XSS <img src=""> attack is removed when embedded tab is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_TAB_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB = {
    'test_id': 1,
    'title': 'Test<IMG SRC="jav&#x09;ascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="jav&#x09;ascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="jav&#x09;ascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="jav&#x09;ascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_embedded_encoded_tab_removed():
    """
    Verify that XSS <img src=""> attack is removed when encoded embedded tab is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_TAB_CLEAN['body']
