# -*- coding: utf-8 -*-
#------------------ help funcions ---------------------------------------------------------



special_char_list = ['.',',',';',':','-','?','!','%','\'','"', '+','*', '%','&','/','(',')','=','?','#',']','['
                            ,'{','}','„', '“','«','»','–','†','\n' ]
digit_list = ['0','1','2','3','4','5','6','7','8','9']

letter_list = ['ä','ö','ü','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                   'Ä','Ö','Ü','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# empty space is part of complete char list
char_list = letter_list + digit_list + special_char_list+ [' ']

special_char_set =set(special_char_list)
digits_set = set(digit_list)
letter_set = set(letter_list)

capital_letter_set = set(['Ä','Ö','Ü','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])

lower_capital_dict = {   'ä':'Ä',
                         'ö':'Ö',
                         'ü':'Ö',
                         'a':'A',
                         'b':'B',
                         'c':'c',
                         'd':'D',
                         'e':'E',
                         'f':'F',
                         'g':'G',
                         'h':'H',
                         'i':'I',
                         'j':'J',
                         'k':'K',
                         'l':'L',
                         'm':'M',
                         'n':'N',
                         'o':'O',
                         'p':'P',
                         'q':'Q',
                         'r':'R',
                         's':'S',
                         't':'T',
                         'u':'U',
                         'v':'V',
                         'w':'W',
                         'x':'X',
                         'y':'Y',
                         'z':'Z'}
# inefficient
def is_digit(string_one):
    return string_one in digits_set

def is_letter(string_one):
    return string_one in letter_set

def is_special_char(string_one):
    return string_one in special_char_set


def next_letter(raw_string,initial_index):

    i = initial_index
    length =len(raw_string)
    while not(is_letter(raw_string[i])):
        i+=1;
        if i==length:
            return None
    return i


def next_sign(raw_string,initial_index):
    '''handles letter and digits'''
    i = initial_index
    length =len(raw_string)
    while not(is_letter(raw_string[i]) and not(is_digit(raw_string[i]))):
        i+=1;
        if i==length:
            return None
    return i


def filter_special_chr_out(my_sting):
    cleanstring = ''
    for i, j in enumerate(my_sting):
        if not(my_sting[i] == '_') and not(my_sting[i] == '"') and not(my_sting[i] == '')  and not(my_sting[i] == '«'):
            cleanstring+= my_sting[i]
    return cleanstring

