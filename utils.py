def check_words_in_list(text, word_list):
    words = text.split()
    return any(word in word_list for word in words)

def replace_words(text, replace_list):
    for word in replace_list:
        text = text.replace(word, "")
    return text