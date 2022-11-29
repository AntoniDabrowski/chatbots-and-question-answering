import json
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('averaged_perceptron_tagger')

english_lemmatizer = WordNetLemmatizer()

with open('./data/polish_lemmas.json', 'r') as file:
    polish_lemmas = json.load(file)

with open('./data/polish_part_of_speech.json', 'r') as file:
    polish_pos = json.load(file)


def word_tokenize(text, lang):
    return text.lower().replace('!', ' ! ').replace('?', ' ? ').replace('.', ' . ').replace(',', ' , ').replace('"',
                                                                                                                '').replace(
        "'", '').replace('|', '').replace(':', '').replace(';', '').replace('(', '').replace(')', '').replace('[',
                                                                                                              '').replace(
        ']', '').replace('/', '').strip().split()


def lemmatize_words(text_arr, lang):
    assert type(text_arr) == list

    res = []

    for word in text_arr:
        if lang == 'pl':
            res.append(polish_lemmas.get(word, word))
        else:
            res.append(english_lemmatizer.lemmatize(word))

    return res


def get_defining_words(words, lang):
    defining_words = []

    if lang == 'pl':
        stop_words = ['co', 'czego', 'czy', 'czyim', 'czyimi', 'czyj', 'czyja', 'czyje',
                      'czyją', 'czym', 'do', 'dokąd', 'gdzie', 'ile', 'ilu', 'jak', 'jaka',
                      'jaki', 'jakie', 'jakiego', 'jakiej', 'jakim', 'jaką', 'kim',
                      'kogo', 'kto', 'która', 'które', 'którego', 'której', 'który',
                      'którą', 'na', 'nad', 'o', 'od', 'pod', 'proszę', 'przez', 'przy',
                      'skąd', 'u', 'w', 'z', 'za']
        defining_words = [word for word in words if
                          polish_pos.get(word, '') in ['subst', 'adj'] and word not in stop_words]
    else:
        defining_words = [word for word, pos in nltk.pos_tag(words) if pos.startswith('NN') or pos.startswith('JJ')]

    return defining_words


def create_query(question, lang):
    assert lang == 'pl' or lang == 'en'

    tokenized = word_tokenize(question, lang)
    lemmatized = lemmatize_words(tokenized, lang)
    defining_words = get_defining_words(lemmatized, lang) if len(lemmatized) > 5 else lemmatized

    return ' '.join(defining_words)