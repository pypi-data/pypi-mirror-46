# todo write a good tokenizer parser function!!
'''
Tokenizer:


- sentence tokenizer
    proceeses sentance sting to tokens, seperated by empty spaces

- sentance finder
    gets unstrucktured texed and divides it into sentances


spesific functionalities

- german corpus tokenizer
    handles the german corpus specific format
'''




#---------------- Sentance finder  -------------------------------------------------------

def get_sentance_raw_txt(raw_string):
    is_sentance = False
    i=0
    for i, c in enumerate(raw_string):
        if c in set(['.','?','!']):
            is_sentance = True
            return is_sentance, raw_string[:i+1], raw_string[i+1:]
    return False, '', raw_string

#--------------- German courpus costum functions -----------------------------------------

def tokenize_germ_courpus(my_sting):
    '''' written for the specific format of the german corupus,
    can handle one or more sentences/lines '''
    cleanstring = filter_special_chr_out(my_sting)
    sentance_list =[]

    end_reached = False
    while not(end_reached):
        sentence_string, cleanstring = get_next_sentance_g_corpus(cleanstring)
        sentance_list.append(tokenize_sentance(sentence_string))
        if cleanstring == '':
            end_reached = True
    return sentance_list


def get_next_sentance_g_corpus(string):
    i=0
    while is_digit(string[i]):
        i+=1
    start =i+1

    reachted_end= False
    while not(reachted_end):
        i += 1
        debugsd=string[i]
        if string[i]=='\n':
            s_end = i
            reachted_end = True

    sentance =string[start:s_end]
    rest_string = string[s_end+2:]
    return sentance, rest_string


