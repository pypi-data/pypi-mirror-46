from test.test_resources.vocabulary_dicts import DE, DE_lower, EN
import pytest
from tokenizer_cstm.determine_language import determine_language


language_col_dict = {
    'DE':DE,
    'EN':EN
}

testdata = [
    (['I'], 'EN'),
    (['ich'], 'DE'),
    (['I', 'amm'], 'EN'),
    (['Ier', 'amm'], None),
    ]


@pytest.mark.parametrize("word_list, language", testdata)
def test_spellcheck(word_list, language):
    probable_lang = determine_language(word_list, language_col_dict)
    assert  probable_lang == language

