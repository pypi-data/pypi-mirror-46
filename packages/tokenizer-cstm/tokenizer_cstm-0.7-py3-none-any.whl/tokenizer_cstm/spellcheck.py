'''
This code is a modivied version of Peter Norvig http://norvig.com/spell-correct.html
for the gensim vocabolary
'''


#from vocab.initialize_gensim_model import vocabulary, WORDS, N
from .help_functions import capital_letter_set, lower_capital_dict, special_char_set


# Costum write functions (pre and after processing


def spellckeck(word, dictionary, lower_case_dictionary):
    "corrects for capitalisation"
    # catch case of no correction
    if word in dictionary:
        return word

    # correction with capital letter
    corrected_word_lower = correction_norvig(word.lower(), lower_case_dictionary)
    if corrected_word_lower == '':
        return ''
    first_char = corrected_word_lower[0]
    if first_char in special_char_set:
        return corrected_word_lower

    if corrected_word_lower.__len__()>1:
        corrected_word_capital = lower_capital_dict[corrected_word_lower[0]]+corrected_word_lower[1:]
    elif corrected_word_lower.__len__()==1:
        corrected_word_capital = lower_capital_dict[corrected_word_lower[0]]
    else:
        return corrected_word_lower



    # choose which one to return
    if (word[0] in capital_letter_set or not(corrected_word_lower in dictionary))\
            and corrected_word_capital in dictionary:
        return corrected_word_capital
    elif corrected_word_lower in dictionary:
        return corrected_word_lower
    return word # nocorrection found




# code from peter Norvig

def correction_norvig(word, dictionary):
    "Most probable spelling correction for word."

    def P(word, N=1):
        "Probability of `word`."
        if word in dictionary:
            return dictionary[word] / N
        else:
            return 0

    return max(candidates(word, dictionary), key=P)

def candidates(word, dictionary):
    "Generate possible spelling corrections for word."
    return (known([word], dictionary) or known(edits1(word), dictionary) or known(edits2(word), dictionary) or [word])

def known(words, dictionary):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in dictionary)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

