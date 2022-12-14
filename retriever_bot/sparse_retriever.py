import morfeusz2
import pickle
from collections import defaultdict as dd
from nltk.tokenize import word_tokenize
import colorama
from termcolor import colored
import numpy as np


def lemmatize_quote(quote, morf):
    analysis = morf.analyse(quote)
    lemmas = dd(set)
    for _, _, token in analysis:
        if ':' in token[1]:
            lemma = token[1].split(':')[0]
        else:
            lemma = token[1]
        if len(lemma) > 3:
            lemmas[token[0].lower()].add(lemma.lower())
    return lemmas

def get_lemmas(word, morf):
    lemmas = set()
    for _, _, lemma in morf.analyse(word):
        if ':' in lemma[1]:
            lemma = lemma[1].split(':')[0]
        else:
            lemma = lemma[1]
        lemmas.add(lemma.lower())
    return lemmas

def match_in_title(tokens, ranking, odwrotny_indeks_titles, title_match, log_matches, importance_const):
    for token in tokens:
        if len(token) > 3:
            article_ids = odwrotny_indeks_titles.get(token.lower(), [])
            importance = importance_const.get('match_in_title', 10) * np.log(1208362 / (len(article_ids) + 1))
            for article_id in article_ids:
                ranking[article_id] += importance
                if log_matches:
                    title_match[article_id].add(token.lower())


def match_in_body(tokens, ranking, odwrotny_indeks_body, body_match, log_matches, importance_const):
    for token in tokens:
        if len(token) > 3:
            article_ids = odwrotny_indeks_body.get(token.lower(), [])
            importance = importance_const.get('match_in_body', 3) * np.log(1208362 / (len(article_ids) + 1))
            for article_id in article_ids:
                ranking[article_id] += importance
                if log_matches:
                    body_match[article_id].add(token.lower())


def lemma_match_in_title(lemmas, ranking, odwrotny_indeks_lematyczny_titles, lemma_title_match, log_matches,
                         importance_const):
    for token in lemmas.keys():
        if len(token) > 3:
            for lemma in lemmas[token]:
                if lemma == 'adam':
                    print(2)
                article_ids = odwrotny_indeks_lematyczny_titles.get(lemma, [])
                importance = importance_const.get('lemma_match_in_title', 5) * np.log(1208362 / (len(article_ids) + 1))
                for article_id in article_ids:
                    ranking[article_id] += importance
                    if log_matches:
                        lemma_title_match[article_id].add(lemma)


def lemma_match_in_body(lemmas, ranking, odwrotny_indeks_lematyczny_body, lemma_body_match, log_matches,
                        importance_const):
    for token in lemmas.keys():
        if len(token) > 3:
            for lemma in lemmas[token]:
                article_ids = odwrotny_indeks_lematyczny_body.get(lemma, [])
                importance = importance_const.get('lemma_match_in_body', 1) * np.log(1208362 / (len(article_ids) + 1))
                for article_id in article_ids:
                    ranking[article_id] += importance
                    if log_matches:
                        lemma_body_match[article_id].add(lemma)


def consider_id(ranking):
    pass
    # for article_id, points in ranking.items():
    #     ranking[article_id] += 1 / (article_id + 2)


def normalization(ranking, body, matches_importance):
    for article_id, v in ranking.items():
        ranking[article_id] = v / (len(body[article_id].split()) + matches_importance.get('normalization', 370))


def get_ranking(query, data, matches_importance={}, log_matches=False):
    odwrotny_indeks_titles, odwrotny_indeks_body, odwrotny_indeks_lematyczny_titles, odwrotny_indeks_lematyczny_body, body, morf = data

    # logging matches
    body_match = dd(set)
    title_match = dd(set)
    lemma_title_match = dd(set)
    lemma_body_match = dd(set)

    ranking = dd(float)

    tokens = word_tokenize(query)

    lemmas = lemmatize_quote(query, morf)

    # ranking computation
    match_in_title(tokens, ranking, odwrotny_indeks_titles, title_match, log_matches, matches_importance)
    match_in_body(tokens, ranking, odwrotny_indeks_body, body_match, log_matches, matches_importance)
    lemma_match_in_title(lemmas, ranking, odwrotny_indeks_lematyczny_titles, lemma_title_match, log_matches,
                         matches_importance)
    lemma_match_in_body(lemmas, ranking, odwrotny_indeks_lematyczny_body, lemma_body_match, log_matches,
                        matches_importance)
    normalization(ranking, body, matches_importance)
    consider_id(ranking)

    if log_matches:
        return ranking, (title_match, body_match, lemma_title_match, lemma_body_match)
    else:
        return ranking


def print_result(article_id, titles, bodies, relevance, matches, morf):
    title_match, body_match, lemma_title_match, lemma_body_match = matches

    print("Relevance:", relevance)
    title = titles[article_id]
    body = bodies[article_id]

    body_matches = body_match.get(article_id, [])
    lemma_body_matches = lemma_body_match.get(article_id, [])
    title_matches = title_match.get(article_id, [])
    lemma_title_matches = lemma_title_match.get(article_id, [])

    new_title = ""
    for word in word_tokenize(title):
        if word.lower() in title_matches:
            new_title += colored(word, 'red') + ' '
        elif get_lemmas(word.lower(), morf).intersection(lemma_title_matches):
            new_title += colored(word, 'magenta') + ' '
        else:
            new_title += word + ' '
    print(new_title)

    new_body = ""
    for paragraph in body.split("\n")[1:]:
        new_paragraph = ""
        for word in word_tokenize(paragraph):
            if word.lower() in body_matches:
                new_paragraph += colored(word, 'blue') + ' '
            elif get_lemmas(word.lower(), morf).intersection(lemma_body_matches):
                new_paragraph += colored(word, 'yellow') + ' '
            else:
                new_paragraph += word + ' '
        new_body += new_paragraph + '\n'

    print(new_body)

if __name__ == '__main__':
    morf = morfeusz2.Morfeusz()
    colorama.init(autoreset=True)

    path = r"C:\Users\user\Studia\Semestr VI\Eksploracja tekstów\Text_mining\dane\wikipedyjka"
    titles = pickle.load(open(path+r'\id_titles.pickle',"rb"))
    body = pickle.load(open(path+r'\id_body.pickle', "rb"))
    odwrotny_indeks_titles = pickle.load(open(path+r'\odwrotny_indeks_titles.pickle',"rb"))
    odwrotny_indeks_body = pickle.load(open(path+r'\odwrotny_indeks_body.pickle',"rb"))
    odwrotny_indeks_lematyczny_titles = pickle.load(open(path+r'\odwrotny_indeks_lematyczny_titles.pickle',"rb"))
    odwrotny_indeks_lematyczny_body = pickle.load(open(path+r'\odwrotny_indeks_lematyczny_body.pickle',"rb"))

    data = (odwrotny_indeks_titles, odwrotny_indeks_body,
            odwrotny_indeks_lematyczny_titles, odwrotny_indeks_lematyczny_body, body, morf)

    matches_importance = {'match_in_title': 9,
                          'lemma_match_in_title': 5,
                          'match_in_body': 2,
                          'lemma_match_in_body': 1}

    print("Możesz zadawać pytania.")
    while True:
        # query = input()
        query = "Adama Mickiewicz"
        # query = 'Jak nazywa się pierwsza litera alfabetu greckiego?'
        ranking, matches = get_ranking(query, data, matches_importance, log_matches=True)

        # choosing best five results
        sorted_results = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
        for article_id, relevance in sorted_results[:300]:
            # if relevance > 0.6:
            print_result(article_id, titles, body, relevance, matches, morf)
        print("Matching:" +
              colored('\nPERFECT MATCH IN TITLE', 'red') +
              colored('\nLEMMA MATCH IN TITLE', 'magenta') +
              colored('\nPERFECT MATCH IN ARTICLE BODY', 'blue') +
              colored('\nLEMMA MATCH IN ARTICLE BODY', 'yellow'))
        break