from tokenizer_cstm.tokenize_sentence import tokenize_sentence
import pytest

# run in terminal (this folder or parent):
# pytest -v
# make sure pytest is installed, run it fom the virtual environment law_project_env




testdata = [
    ('Hallo, wie geht es dir?',['Hallo', ',', 'wie', 'geht', 'es', 'dir', '?']),
    ('Mir geht es gut, Danke!',['Mir', 'geht', 'es', 'gut', ',', 'Danke', '!']),
    ('',[]),
    ('Mir geht es gut (sehr gut)!',['Mir', 'geht', 'es', 'gut','(','sehr','gut',')', '!']),
    ('Er sagte:"keine Ahnung!?"',['Er', 'sagte', ':', '"','keine','Ahnung','!','?','"']),
    ('später vor allem in Indonesien („Gewürzinseln“).',
     ['später', 'vor', 'allem', 'in', 'Indonesien', '(', '„', 'Gewürzinseln', '“', ')', '.']),
    ('ich wiege 12.23 oder 13,2 Kilo', ['ich','wiege' ,'12.23', 'oder', '13,2', 'Kilo']),
    ('wie 2?', ['wie','2' ,'?']),
    ('.2.', ['.','2' ,'.']),
    ('1.2', ['1.2']),
    ('',[]),
    ('Zone\n', ['Zone', '\n'])
    ]

@pytest.mark.parametrize("sentance, tokens", testdata)
def test_tokenize_sentance(sentance, tokens):
    tokens_found, _,_ = tokenize_sentence(sentance)
    assert tokens_found == tokens

testdata = [
    ('Hallo, wie geht es dir?',[0, 5, 7, 11, 16, 19, 22]),
    ('ich wiege 12.23 oder 13,2 Kilo', [0,4,10,16,21,26]),
    ('',[])
    ]

@pytest.mark.parametrize("sentance, indexes", testdata)
def test_tokenize_sentance_indexes(sentance, indexes):
    _, indexes_found,_ = tokenize_sentence(sentance)
    assert indexes_found == indexes



testdata = [
    ('Hallo, wie geht es dir?',[4, 5, 9, 14, 17, 21, 22]),
    ('ich wiege 12.23 oder 13,2 Kilo', [2,8,14,19,24,29]),
    ('',[])
    ]

@pytest.mark.parametrize("sentance, indexes", testdata)
def test_tokenize_sentance_indexes(sentance, indexes):
    _, _, indexes_found = tokenize_sentence(sentance)
    assert indexes_found == indexes
