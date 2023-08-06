"""
Test simple and genuine input from a trusted user against the filters.
"""
import pytest
from testapp.models import TestModel


TEST_DATA_VALID_HTML = {
    'test_id': 1,
    'title': 'A Lonely Pigeon',
    'description': 'A story I wrote just for this test.',
    'byline': '<i>A story about a bird with no friends.</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '\n\n'
            'Once upon a time, there was a pigeon named Steve. Steve didn\'t have'
            ' any friends. No one wanted to be near him because of his love of rotten sardines, and who could'
            ' blame them? Sardines smelled a bit strong when they were fresh, but rotten sardines were enough '
            'to bring tears to the eyes of the most vicious savage.'
            '\n\n'
            '    When Steve flew down the street, flowers in planter boxes would wilt under the power of his '
            'breath. His wingtips were usually covered in the oily remains of decomposing fish he eagerly '
            'shoved into his beak whenever he located some sardines. The bits would rain down on the people '
            'on the street as he took of after a fresh meal. Most people found an awning to duck under '
            'whenever they saw Steve.'
            '\n\n'
            '    Fortunately, Steve was easily identifiable by the mushroom shaped black spot he had over his '
            'left eye. This allowed people to avoid him.'
            '\n\n'
            'Barney, the local shopkeep was walking down the street when suddenly he heard a flapping of '
            'wings from behind him. He looked behind him, and coming out of the dumpster from the alleyway '
            'was Steve.'
            '\n\n'
            '"<em>Bloody hell!</em>" exclaimed Barney. "I\'d better find cover and fast."'
            '\n\n'
            'Barney dove under the awning in front of the newspaper stand, knocking down the stack of '
            'newspapers that Mrs Black had just finished stacking for the day.'
            '\n\n'
            '"<i>Barney! My newspapers!</i>" yelled Mrs Black.'
            '\n\n'
            '"<strong>Sorry!</strong>" Barney replied as he watched Steve fly by, "but that blasted bird was '
            'a comin\' down the way. I <b>had</b> to find cover."'
            '<pagebreak></pagebreak>'
}

TEST_DATA_INVALID_HTML = {
    'test_id': 1,
    'title': 'A Lonely <div></div>Pigeon',
    'description': 'A story I wrote just for this test.',
    'byline': '<i>A story about a bird with no friends.</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '\n\n'
            'Once upon a time, there was a pigeon named Steve. Steve didn\'t have'
            ' any friends. No one wanted to be near him because of his love of rotten sardines, and who could'
            ' blame them? Sardines smelled a bit strong when they were fresh, but rotten sardines were enough '
            'to bring tears to the eyes of the most vicious savage.'
            '\n\n'
            '    When Steve flew down the street, flowers in planter boxes would wilt under the power of his '
            'breath. His wingtips were usually covered in the oily remains of decomposing fish he eagerly '
            'shoved into his beak whenever he located some sardines. The bits would rain down on the people '
            'on the street as he took of after a fresh meal. Most people found an awning to duck under '
            'whenever they saw Steve.'
            '\n\n'
            '    Fortunately, Steve was easily identifiable by the mushroom shaped black spot he had over his '
            'left eye. This allowed people to avoid him.'
            '\n\n'
            'Barney, the local shopkeep was walking down the street when suddenly he heard a flapping of '
            'wings from behind him. He looked behind him, and coming out of the dumpster from the alleyway '
            'was Steve.'
            '\n\n'
            '"<em>Bloody hell!</em>" exclaimed Barney. "I\'d better find cover and fast."'
            '\n\n'
            'Barney dove under the awning in front of the newspaper stand, knocking down the stack of '
            'newspapers that Mrs Black had just finished stacking for the day.'
            '\n\n'
            '<form name="form1" method="post" action="badstuff.php" id="form1">'
            '<input type="text" name="test" id="test" value="badstuff" />'
            '</form>'
            '<div></div>'
            '"<i>Barney! My newspapers!</i>" yelled Mrs Black.'
            '\n\n'
            '"<strong>Sorry!</strong>" Barney replied as he watched Steve fly by, "but that blasted bird was '
            'a comin\' down the way. I <b>had</b> to find cover."'
            '<pagebreak />'
}

TEST_DATA_SCRIPT_TAGS = {
    'test_id': 1,
    'title': 'A Lonely Pigeon',
    'description': 'A story I wrote just for this test.',
    'byline': '<i>A story about a bird with no friends.</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '\n\n'
            '<script type="text/javascript">'
            '    $(document).ready(function (event) {'
            '        $(\'#txt_input\').keyup(function (event) {'
            '            $(\'#div_html_result\').html($(\'#txt_input\').val())'
            '        })'
            '        $(\'#txt_input\').focusout(function (event) {'
            '            $(\'#div_html_result\').html($(\'#txt_input\').val())'
            '        })'
            '        $(\'#txt_input\').focusin(function (event) {'
            '            $(\'#div_html_result\').html($(\'#txt_input\').val())'
            '        })'
            '        $(\'#btn_result\').click(function (event) {'
            '            $(\'#div_html_result\').html($(\'#txt_input\').val())'
            '            return false;'
            '        })'
            '    });'
            '</script>'
            'Once upon a time, there was a pigeon named Steve. Steve didn\'t have'
            ' any friends. No one wanted to be near him because of his love of rotten sardines, and who could'
            ' blame them? Sardines smelled a bit strong when they were fresh, but rotten sardines were enough '
            'to bring tears to the eyes of the most vicious savage.'
            '\n\n'
            '    When Steve flew down the street, flowers in planter boxes would wilt under the power of his '
            'breath. His wingtips were usually covered in the oily remains of decomposing fish he eagerly '
            'shoved into his beak whenever he located some sardines. The bits would rain down on the people '
            'on the street as he took of after a fresh meal. Most people found an awning to duck under '
            'whenever they saw Steve.'
            '\n\n'
            '    Fortunately, Steve was easily identifiable by the mushroom shaped black spot he had over his '
            'left eye. This allowed people to avoid him.'
            '\n\n'
            'Barney, the local shopkeep was walking down the street when suddenly he heard a flapping of '
            'wings from behind him. He looked behind him, and coming out of the dumpster from the alleyway '
            'was Steve.'
            '\n\n'
            '"<em>Bloody hell!</em>" exclaimed Barney. "I\'d better find cover and fast."'
            '\n\n'
            'Barney dove under the awning in front of the newspaper stand, knocking down the stack of '
            'newspapers that Mrs Black had just finished stacking for the day.'
            '\n\n'
            '"<i>Barney! My newspapers!</i>" yelled Mrs Black.'
            '\n\n'
            '"<strong>Sorry!</strong>" Barney replied as he watched Steve fly by, "but that blasted bird was '
            'a comin\' down the way. I <b>had</b> to find cover."'
            '<pagebreak></pagebreak>'
}

TEST_DATA_STYLE_TAGS = {
    'test_id': 1,
    'title': 'A Lonely Pigeon',
    'description': 'A story I wrote just for this test.',
    'byline': '<i>A story about a bird with no friends.</i>',
    'body': '<span class="underlined-subtitle" style="text-decoration: underline; font-size: 20px;">Chapter 1</span>'
            '\n\n'
            '<style>'
            '    body { font-family: arial,sans-serif; background-color: #131313; '
            '    color: seashell; padding: 10px 100px; max-width: 1000px; margin: auto; }'
            '    a { text-decoration: none; color: darkgreen; }'
            '    h2 { color: darkgreen }'
            '    img { border:none; }'
            '</style>'
            'Once upon a time, there was a pigeon named Steve. Steve didn\'t have'
            ' any friends. No one wanted to be near him because of his love of rotten sardines, and who could'
            ' blame them? Sardines smelled a bit strong when they were fresh, but rotten sardines were enough '
            'to bring tears to the eyes of the most vicious savage.'
            '\n\n'
            '    When Steve flew down the street, flowers in planter boxes would wilt under the power of his '
            'breath. His wingtips were usually covered in the oily remains of decomposing fish he eagerly '
            'shoved into his beak whenever he located some sardines. The bits would rain down on the people '
            'on the street as he took of after a fresh meal. Most people found an awning to duck under '
            'whenever they saw Steve.'
            '\n\n'
            '    Fortunately, Steve was easily identifiable by the mushroom shaped black spot he had over his '
            'left eye. This allowed people to avoid him.'
            '\n\n'
            'Barney, the local shopkeep was walking down the street when suddenly he heard a flapping of '
            'wings from behind him. He looked behind him, and coming out of the dumpster from the alleyway '
            'was Steve.'
            '\n\n'
            '"<em>Bloody hell!</em>" exclaimed Barney. "I\'d better find cover and fast."'
            '\n\n'
            'Barney dove under the awning in front of the newspaper stand, knocking down the stack of '
            'newspapers that Mrs Black had just finished stacking for the day.'
            '\n\n'
            '"<i>Barney! My newspapers!</i>" yelled Mrs Black.'
            '\n\n'
            '"<strong>Sorry!</strong>" Barney replied as he watched Steve fly by, "but that blasted bird was '
            'a comin\' down the way. I <b>had</b> to find cover."'
            '<pagebreak></pagebreak>'
}


@pytest.mark.django_db
def test_valid_html_is_preserved():
    """
    Verify that properly formatted HTML is not broken or removed.
    """
    TestModel.objects.create(**TEST_DATA_VALID_HTML)
    sample = TestModel.objects.get(test_id=1)
    assert sample.title == TEST_DATA_VALID_HTML['title']
    assert sample.description == TEST_DATA_VALID_HTML['description']
    assert sample.byline == TEST_DATA_VALID_HTML['byline']
    assert sample.body == TEST_DATA_VALID_HTML['body']


@pytest.mark.django_db
def test_invalid_html_is_fixed_or_removed():
    """
    Verify that only allowed tags get through the filter.
    """
    TestModel.objects.create(**TEST_DATA_INVALID_HTML)
    sample = TestModel.objects.get(test_id=1)
    assert sample.title == TEST_DATA_VALID_HTML['title']
    assert sample.description == TEST_DATA_VALID_HTML['description']
    assert sample.byline == TEST_DATA_VALID_HTML['byline']
    assert sample.body == TEST_DATA_VALID_HTML['body']


@pytest.mark.django_db
def test_script_tags_and_contents_removed():
    """
    Verify that <script> tags and their contents are completely removed.
    """
    TestModel.objects.create(**TEST_DATA_SCRIPT_TAGS)
    sample = TestModel.objects.get(test_id=1)
    assert sample.title == TEST_DATA_VALID_HTML['title']
    assert sample.description == TEST_DATA_VALID_HTML['description']
    assert sample.byline == TEST_DATA_VALID_HTML['byline']
    assert sample.body == TEST_DATA_VALID_HTML['body']


@pytest.mark.django_db
def test_style_tags_and_contents_removed():
    """
    Verify that <style> tags and their contents are completely removed.
    """
    TestModel.objects.create(**TEST_DATA_STYLE_TAGS)
    sample = TestModel.objects.get(test_id=1)
    assert sample.title == TEST_DATA_VALID_HTML['title']
    assert sample.description == TEST_DATA_VALID_HTML['description']
    assert sample.byline == TEST_DATA_VALID_HTML['byline']
    assert sample.body == TEST_DATA_VALID_HTML['body']
