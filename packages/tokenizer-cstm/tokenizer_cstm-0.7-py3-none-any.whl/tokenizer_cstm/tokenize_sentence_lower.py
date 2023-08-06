from .tokenize_sentence import tokenize_sentence

def tokenize_sentence_lower(sentence_string):
    tokens, _, _ = tokenize_sentence(sentence_string=sentence_string)
    tokens_lower = []
    for token in tokens:
        tokens_lower.append(token.lower())
    return tokens_lower