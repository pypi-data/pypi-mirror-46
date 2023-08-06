import pytest
from tokenizer_cstm.help_functions import next_letter

testdata = [
    (' Hallo wie geht es dir?', 0, 1),
    (' Hallo wie geht es dir?', 1, 1),
    (' Hallo wie geht es dir?', 22, None),
    ('324:;är323!', 0, 5),
    ('324:;är323!', 7, None),
    ('3', 0, None),
    ]


@pytest.mark.parametrize("string, initial_index, index", testdata)
def test_next_letter(string, initial_index, index):
    assert next_letter(string, initial_index) == index