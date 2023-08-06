"""
Test OWASP attacks against parser.
"""
import pytest
from testapp.models import XSSModel


TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE = {
    'test_id': 1,
    'title': 'Test<IMG SRC="jav&#x0A;ascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="jav&#x0A;ascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="jav&#x0A;ascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="jav&#x0A;ascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_embedded_encoded_newline_removed():
    """
    Verify that XSS <img src=""> attack is removed when embedded newline is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_NEWLINE_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN = {
    'test_id': 1,
    'title': 'Test<IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="jav&#x0D;ascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_embedded_encoded_carriage_return_removed():
    """
    Verify that XSS <img src=""> attack is removed when embedded carriage return is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_ENCODED_CARRIAGE_RETURN_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="jav">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="jav">'
}

TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL = {
    'test_id': 1,
    'title': 'Test<IMG SRC="jav\0ascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC="jav\0ascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="jav\0ascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="jav\0ascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_embedded_null_removed():
    """
    Verify that XSS <img src=""> attack is removed when embedded null is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_EMBEDDED_NULL_CLEAN['body']


TEST_OWASP_XSS_IMG_SRC_META_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_SRC_META = {
    'test_id': 1,
    'title': 'Test<IMG SRC=" &#14;  javascript:alert(\'XSS\');">',
    'description': 'Testing<IMG SRC=" &#14;  javascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=" &#14;  javascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=" &#14;  javascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_src_meta_removed():
    """
    Verify that XSS <img src=""> attack is removed when spaces and meta chars are present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_SRC_META)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_SRC_META_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_SRC_META_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_SRC_META_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_SRC_META_CLEAN['body']


TEST_OWASP_XSS_NON_ALPHA_DIGIT_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_NON_ALPHA_DIGIT = {
    'test_id': 1,
    'title': 'Test<SCRIPT/XSS SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'description': 'Testing<SCRIPT/XSS SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT/XSS SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><SCRIPT/XSS SRC="http://xss.rocks/xss.js"></SCRIPT>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_non_alpha_digit_removed():
    """
    Verify that XSS script attack is removed when non-alpha-non-digit is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_NON_ALPHA_DIGIT)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_NON_ALPHA_DIGIT_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_NON_ALPHA_DIGIT_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_NON_ALPHA_DIGIT_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_NON_ALPHA_DIGIT_CLEAN['body']


TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE = {
    'test_id': 1,
    'title': 'Test<SCRIPT/SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'description': 'Testing<SCRIPT/SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT/SRC="http://xss.rocks/xss.js"></SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><SCRIPT/SRC="http://xss.rocks/xss.js"></SCRIPT>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_non_alpha_digit_no_space_removed():
    """
    Verify that XSS script attack is removed when non-alpha-non-digit with no space is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_NON_ALPHA_DIGIT_NO_SPACE_CLEAN['body']


TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS_CLEAN = {
    'test_id': 1,
    'title': 'Test&lt;',
    'description': 'Testing&lt;',
    'byline': '<i>A very basic model for OWASP tests</i>&lt;',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>&lt;'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS = {
    'test_id': 1,
    'title': 'Test<<SCRIPT>alert("XSS");//<</SCRIPT>',
    'description': 'Testing<<SCRIPT>alert("XSS");//<</SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i><<SCRIPT>alert("XSS");//<</SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><<SCRIPT>alert("XSS");//<</SCRIPT>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_extra_open_brackets_removed():
    """
    Verify that XSS script attack is removed when extraneous open brackets are present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_EXTRA_OPEN_BRACKETS_CLEAN['body']


TEST_OWASP_XSS_NO_CLOSING_TAG_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
}

TEST_OWASP_XSS_NO_CLOSING_TAG = {
    'test_id': 1,
    'title': 'Test<SCRIPT SRC=http://xss.rocks/xss.js?< B >',
    'description': 'Testing<SCRIPT SRC=http://xss.rocks/xss.js?< B >',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT SRC=http://xss.rocks/xss.js?< B >',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><SCRIPT SRC=http://xss.rocks/xss.js?< B >'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_no_closing_tag_removed():
    """
    Verify that XSS script attack is removed when no closing tag is present.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_NO_CLOSING_TAG)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_NO_CLOSING_TAG_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_NO_CLOSING_TAG_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_NO_CLOSING_TAG_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_NO_CLOSING_TAG_CLEAN['body']


TEST_OWASP_XSS_PROTOCOL_RESOLUTION_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
}

TEST_OWASP_XSS_PROTOCOL_RESOLUTION = {
    'test_id': 1,
    'title': 'Test<SCRIPT SRC=//xss.rocks/.j>',
    'description': 'Testing<SCRIPT SRC=//xss.rocks/.j>',
    'byline': '<i>A very basic model for OWASP tests</i><SCRIPT SRC=//xss.rocks/.j>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><SCRIPT SRC=//xss.rocks/.j>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_protocol_resolution_removed():
    """
    Verify that XSS script attack is removed when no closing tag is present and protocol is left off.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_PROTOCOL_RESOLUTION)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_PROTOCOL_RESOLUTION_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_PROTOCOL_RESOLUTION_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_PROTOCOL_RESOLUTION_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_PROTOCOL_RESOLUTION_CLEAN['body']


TEST_OWASP_XSS_HALF_OPEN_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
}

TEST_OWASP_XSS_HALF_OPEN = {
    'test_id': 1,
    'title': 'Test<IMG SRC="javascript:alert(\'XSS\')"',
    'description': 'Testing<IMG SRC="javascript:alert(\'XSS\')"',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC="javascript:alert(\'XSS\')"',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC="javascript:alert(\'XSS\')"'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_half_open_removed():
    """
    Verify that XSS script attack is removed when opening tag is not complete.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_HALF_OPEN)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_HALF_OPEN_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_HALF_OPEN_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_HALF_OPEN_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_HALF_OPEN_CLEAN['body']


TEST_OWASP_XSS_DOUBLE_OPEN_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
}

TEST_OWASP_XSS_DOUBLE_OPEN = {
    'test_id': 1,
    'title': 'Test<iframe src=http://xss.rocks/scriptlet.html <',
    'description': 'Testing<iframe src=http://xss.rocks/scriptlet.html <',
    'byline': '<i>A very basic model for OWASP tests</i><iframe src=http://xss.rocks/scriptlet.html <',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><iframe src=http://xss.rocks/scriptlet.html <'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_double_open_removed():
    """
    Verify that XSS script attack is removed when opening tag has double open angle brackets.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_DOUBLE_OPEN)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_DOUBLE_OPEN_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_DOUBLE_OPEN_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_DOUBLE_OPEN_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_DOUBLE_OPEN_CLEAN['body']


TEST_OWASP_XSS_END_TITLE_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_END_TITLE = {
    'test_id': 1,
    'title': 'Test</TITLE><SCRIPT>alert("XSS");</SCRIPT>',
    'description': 'Testing</TITLE><SCRIPT>alert("XSS");</SCRIPT>',
    'byline': '<i>A very basic model for OWASP tests</i></TITLE><SCRIPT>alert("XSS");</SCRIPT>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b></TITLE><SCRIPT>alert("XSS");</SCRIPT>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_end_title_removed():
    """
    Verify that XSS script attack is removed when content has a </title> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_END_TITLE)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_END_TITLE_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_END_TITLE_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_END_TITLE_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_END_TITLE_CLEAN['body']


TEST_OWASP_XSS_INPUT_IMG_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_INPUT_IMG = {
    'test_id': 1,
    'title': 'Test<INPUT TYPE="IMAGE" SRC="javascript:alert(\'XSS\');">',
    'description': 'Testing<INPUT TYPE="IMAGE" SRC="javascript:alert(\'XSS\');">',
    'byline': '<i>A very basic model for OWASP tests</i><INPUT TYPE="IMAGE" SRC="javascript:alert(\'XSS\');">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><INPUT TYPE="IMAGE" SRC="javascript:alert(\'XSS\');">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_input_img_removed():
    """
    Verify that XSS script attack is removed when content has an <input type="image"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_INPUT_IMG)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_INPUT_IMG_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_INPUT_IMG_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_INPUT_IMG_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_INPUT_IMG_CLEAN['body']


TEST_OWASP_XSS_BODY_IMG_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_BODY_IMG = {
    'test_id': 1,
    'title': 'Test<BODY BACKGROUND="javascript:alert(\'XSS\')">',
    'description': 'Testing<BODY BACKGROUND="javascript:alert(\'XSS\')">',
    'byline': '<i>A very basic model for OWASP tests</i><BODY BACKGROUND="javascript:alert(\'XSS\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><BODY BACKGROUND="javascript:alert(\'XSS\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_body_img_removed():
    """
    Verify that XSS script attack is removed when content has an <body background="xss"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_BODY_IMG)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_BODY_IMG_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_BODY_IMG_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_BODY_IMG_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_BODY_IMG_CLEAN['body']


TEST_OWASP_XSS_IMG_DYNSRC_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_DYNSRC = {
    'test_id': 1,
    'title': 'Test<IMG DYNSRC="javascript:alert(\'XSS\')">',
    'description': 'Testing<IMG DYNSRC="javascript:alert(\'XSS\')">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG DYNSRC="javascript:alert(\'XSS\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG DYNSRC="javascript:alert(\'XSS\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_dynsrc_removed():
    """
    Verify that XSS script attack is removed when content has an <img dynsrc="xss"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_DYNSRC)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_DYNSRC_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_DYNSRC_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_DYNSRC_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_DYNSRC_CLEAN['body']


TEST_OWASP_XSS_IMG_LOWSRC_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img>'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_IMG_LOWSRC = {
    'test_id': 1,
    'title': 'Test<IMG LOWSRC="javascript:alert(\'XSS\')">',
    'description': 'Testing<IMG LOWSRC="javascript:alert(\'XSS\')">',
    'byline': '<i>A very basic model for OWASP tests</i><IMG LOWSRC="javascript:alert(\'XSS\')">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG LOWSRC="javascript:alert(\'XSS\')">'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_img_lowsrc_removed():
    """
    Verify that XSS script attack is removed when content has an <img lowsrc="xss"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_IMG_LOWSRC)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_IMG_LOWSRC_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_IMG_LOWSRC_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_IMG_LOWSRC_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_IMG_LOWSRC_CLEAN['body']


TEST_OWASP_XSS_LI_STYLE_IMG_CLEAN = {
    'test_id': 1,
    'title': 'TestXSS',
    'description': 'TestingXSS',
    'byline': '<i>A very basic model for OWASP tests</i><style>li {list-style-image: url("");}</style>'
              '<ul><li>XSS</li></ul>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><style>li {list-style-image: url("");}</style><ul><li>XSS'
            '<pagebreak></pagebreak></li></ul>'
}

TEST_OWASP_XSS_LI_STYLE_IMG = {
    'test_id': 1,
    'title': 'Test<STYLE>li {list-style-image: url("javascript:alert(\'XSS\')");}</STYLE><UL><LI>XSS</br>',
    'description': 'Testing<STYLE>li {list-style-image: url("javascript:alert(\'XSS\')");}</STYLE><UL><LI>XSS</br>',
    'byline': '<i>A very basic model for OWASP tests</i><STYLE>li {list-style-image: url("javascript:alert(\'XSS\')");}</STYLE><UL><LI>XSS</br>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><STYLE>li {list-style-image: url("javascript:alert(\'XSS\')");}</STYLE><UL><LI>XSS</br>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_li_style_img_removed():
    """
    Verify that XSS script attack is removed when content has an <img lowsrc="xss"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_LI_STYLE_IMG)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_LI_STYLE_IMG_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_LI_STYLE_IMG_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_LI_STYLE_IMG_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_LI_STYLE_IMG_CLEAN['body']


TEST_OWASP_XSS_VBSCRIPT_IMG_CLEAN = {
    'test_id': 1,
    'title': 'Test',
    'description': 'Testing',
    'byline': '<i>A very basic model for OWASP tests</i><img src="">',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><img src="">'
            '<pagebreak></pagebreak>'
}

TEST_OWASP_XSS_VBSCRIPT_IMG = {
    'test_id': 1,
    'title': 'Test<IMG SRC=\'vbscript:msgbox("XSS")\'>',
    'description': 'Testing<IMG SRC=\'vbscript:msgbox("XSS")\'>',
    'byline': '<i>A very basic model for OWASP tests</i><IMG SRC=\'vbscript:msgbox("XSS")\'>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '<b>Just testing</b><IMG SRC=\'vbscript:msgbox("XSS")\'>'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_xss_vbscript_img_removed():
    """
    Verify that XSS script attack is removed when content has an <img lowsrc="xss"> tag.
    """
    XSSModel.objects.create(**TEST_OWASP_XSS_VBSCRIPT_IMG)
    sample = XSSModel.objects.get(test_id=1)
    assert sample.title == TEST_OWASP_XSS_VBSCRIPT_IMG_CLEAN['title']
    assert sample.description == TEST_OWASP_XSS_VBSCRIPT_IMG_CLEAN['description']
    assert sample.byline == TEST_OWASP_XSS_VBSCRIPT_IMG_CLEAN['byline']
    assert sample.body == TEST_OWASP_XSS_VBSCRIPT_IMG_CLEAN['body']
