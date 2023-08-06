

def determine_language(word_list, language_col_dict):
    max_occurance = 0
    key_max = None

    for key in language_col_dict:
        current_occruance = number_of_occurance(word_list,language_col_dict[key])
        if current_occruance == max_occurance:
            key_max = None
        if current_occruance > max_occurance:
            key_max = key
            max_occurance = current_occruance
    return key_max



def number_of_occurance(word_list, language_dict):
    wordcount = 0
    for word in word_list:
        if word in language_dict:
            wordcount += 1
    return wordcount


