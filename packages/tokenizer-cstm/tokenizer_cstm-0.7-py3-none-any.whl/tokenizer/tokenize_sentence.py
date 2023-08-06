from .help_functions import is_special_char, is_digit
#------------- Sentance tokenizer ------------------
# todo tokenizer consider numbers!





def tokenize_sentence(sentence_string):
    tokenizer = Tokeniser(sentence_string)
    return tokenizer.tokenize_sentence_c()


class Tokeniser():
    def __init__(self, sentence_string):
        self.sentence_string = sentence_string
        self.sentance_list = []
        self.start_index_list = []
        self.end_index_list = []
        self.currentWord = ''
        self.open_word = False

    def tokenize_sentence_c(self):
        for i, l in enumerate(self.sentence_string):
            self.check_start_word( i, l)
            if l == ' ':
                self.handl_space(i,l)
                continue
            if is_special_char(l) and not (is_in_numbers(i, self.sentence_string)):
                if self.currentWord == '':
                    self.sentance_list.append(l)
                    self.end_index_list.append(i)
                    continue
                else:
                    self.sentance_list.append(self.currentWord)
                    self.end_index_list.append(i - 1)
                    self.sentance_list.append(l)
                    self.start_index_list.append(i)
                    self.end_index_list.append(i)
                    self.currentWord = ''
                    continue
            self.currentWord += l

        if not (self.currentWord == ''):  # add last word
            self.sentance_list.append(self.currentWord)
            self.end_index_list.append(len(self.sentence_string)-1)
        return self.sentance_list, self.start_index_list, self.end_index_list


    def handl_space(self, i,l):
        if self.currentWord == '':
            pass
        else:
            self.sentance_list.append(self.currentWord)
            self.end_index_list.append(i - 1)
            self.currentWord = ''


    def check_start_word(self,i,l):
        if self.currentWord == '' and not(l == ' '):
            self.start_index_list.append(i)


def is_in_numbers(i, sentancesting):
    if sentancesting[i] in [',','.']:
        if is_digit(sentancesting[i-1]):
            if i+1 < sentancesting.__len__() and is_digit(sentancesting[i+1]):
                return True
    return False




