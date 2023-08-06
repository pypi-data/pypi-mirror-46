import pytest
from tokenizer_cstm.sentence_finder import sentence_finder

# todo digints with punktuation.
# digits and abrehention at the end of a sentance


testdata = [
     ('345', ['345']),
    ('das sehe \nich so', ['das sehe \nich so']),
     (' Hallo wie geht es dir? Heute ist ein schöner Tag! Das sehe ich auch so.',
     ['Hallo wie geht es dir?',
      'Heute ist ein schöner Tag!',
      'Das sehe ich auch so.']),
    ('', []),

    ]


@pytest.mark.parametrize("raw_text, sentances", testdata)
def test_sentence_finder(raw_text, sentances):
    assert set(sentence_finder(raw_text,'DE')) == set(sentances)


## Abrehentions
testdata = [
    (' Dieses Bergtahl, welches auf 1000 M.ü.M. liegt, ist schön.',
     ['Dieses Bergtahl, welches auf 1000 M.ü.M. liegt, ist schön.']),
    (' Dieses Bergtahl liegt auf 1000 M.ü.M..', ['Dieses Bergtahl liegt auf 1000 M.ü.M..']),
    (' Dieses Bergtahl liegt auf 1000 M.ü.M.', ['Dieses Bergtahl liegt auf 1000 M.ü.M.']) # at the end of raw_text
]
@pytest.mark.parametrize("raw_text, sentances", testdata)
def test_sentence_finder_abrehentions(raw_text, sentances):
    assert set(sentence_finder(raw_text,'DE')) == set(sentances)

# Numbers
## Abrehentions
testdata = [
    (' Das wiegt 23.124 Kilos. Es ist das 1. Gewicht auf der Wage.',
     ['Das wiegt 23.124 Kilos.', 'Es ist das 1. Gewicht auf der Wage.']),
]
@pytest.mark.parametrize("raw_text, sentances", testdata)
def test_sentence_finder_digits(raw_text, sentances):
    assert set(sentence_finder(raw_text,'DE')) == set(sentances)