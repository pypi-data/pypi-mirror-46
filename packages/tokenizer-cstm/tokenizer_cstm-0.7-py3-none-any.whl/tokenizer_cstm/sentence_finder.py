from .help_functions import next_letter,next_sign, is_digit, is_letter


#---------------- Sentance finder  -------------------------------------------------------

def sentence_finder(raw_string, laender_string= "DE"):
    init_ind=0
    sentence_list = []
    if raw_string=='' : # handle empty case
        return sentence_list
    raw_string = raw_string[next_letter(raw_string,init_ind):] # start with the first Letter# todo maybe inefficient
    for i, c in enumerate(raw_string):
        if c == '.':
            sentance_breack, extra_jump = is_sentance_point(raw_string, i)
            if sentance_breack:
                sentence_list.append(raw_string[init_ind:i + 1+ extra_jump])
                init_ind = next_letter(raw_string, i)
        if c == '?' or c == '!': # todo maybe consider expressions like ?!
            sentence_list.append(raw_string[init_ind:i+1])
            init_ind = next_sign(raw_string,i)
    if not(init_ind==None):
        sentence_list.append(raw_string[init_ind:])
    return sentence_list


def is_sentance_point(raw_string, i):
    if is_digit(raw_string[i-1]): # todo handles number at end of sentance incorrectly
        return False , 0
    if is_abbreviation(raw_string,i):
        if i == len(raw_string)-1 or raw_string[i+1] == '.': # case of abbreviation at the sentence end # python indexing
            return True, 1
        else:
            return False, 0
    return True, 0


def is_abbreviation(raw_string,i):
    if i<2:
        return True
    if is_letter(raw_string[i-1]) and not (is_letter(raw_string[i-2])):
        return True
    # todo make a look up set of abbreviation for bigger abbreviations
    return False
