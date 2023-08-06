from test.test_resources.vocabulary_dicts import DE, DE_lower
import pytest
from tokenizer_cstm.spellcheck import spellckeck

testdata = [
    ('ick', 'ich'),
    ('izk', 'ich'),
    ('ich','ich'),
    ('Hans','Hans'),
    ('hans','Hans'),
    ('Hank','Hans'),
    ('sdfsdf','sdfsdf'),
    ('renne', 'renne'),
    ('?','?'),
    ('',''),
    ('?was','?was')
    ]


@pytest.mark.parametrize("word, correction", testdata)
def test_spellcheck(word, correction):

    assert spellckeck(word, DE, DE_lower) == correction

