from tokenizer_cstm.tokenize_sentence_lower import tokenize_sentence_lower
import pytest

# run in terminal (this folder or parent):
# pytest -v
# make sure pytest is installed, run it fom the virtual environment law_project_env




testdata = [
    ('Hallo, wie \ngeht es dir?',['hallo', ',', 'wie', '\n','geht', 'es', 'dir', '?']),
    ('d’invalidité', ['d','’','invalidité']),
    ('Mir geht es gut, Danke!',['mir', 'geht', 'es', 'gut', ',', 'danke', '!']),
    ('mit	übertritt	vom	renten',['mit', 'übertritt', 'vom', 'renten']),
    ('',[]),
    ('Mir geht es gut (sehr gut)!',['mir', 'geht', 'es', 'gut','(','sehr','gut',')', '!']),
    ('Er sagte:"keine Ahnung!?"',['er', 'sagte', ':', '"','keine','ahnung','!','?','"']),
    ('später vor allem in Indonesien („Gewürzinseln“).',
     ['später', 'vor', 'allem', 'in', 'indonesien', '(', '„', 'gewürzinseln', '“', ')', '.']),
    ('ich wiege 12.23 oder 13,2 Kilo', ['ich','wiege' ,'12.23', 'oder', '13,2', 'kilo']),
    ('wie 2?', ['wie','2' ,'?']),
    ('.2.', ['.','2' ,'.']),
    ('1.2', ['1.2']),
    ('',[]),
    ('Zone\n', ['zone', '\n'])
    ]

@pytest.mark.parametrize("sentance, tokens", testdata)
def test_tokenize_sentance(sentance, tokens):
    tokens_found= tokenize_sentence_lower(sentance)
    assert tokens_found == tokens