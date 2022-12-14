from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
import numpy as np


def prep_sentence(sentence, w2v):
    restrictions = lambda word: len(word) > 3 and word in w2v
    return [word.lower() for word in word_tokenize(sentence) if restrictions(word.lower())]


def get_sim_arr(query, body, w2v):
    arr = []
    for word_body in body:
        if len(word_body) > 3:
            for word_query in query:
                if len(word_query) > 3:
                    arr.append(max([w2v.similarity(word_body.lower(), word_query.lower())]))
    return arr


def article_arr_score(scores):
    return np.mean(sorted(scores, reverse=True)[:(min(5, len(scores)))])


def article_score(body, query, w2v):
    q = prep_sentence(query, w2v)
    b = prep_sentence(body, w2v)
    return article_arr_score(get_sim_arr(q, b, w2v))


if __name__ == '__main__':
    bodies = [
        'Mickiewicz\n\nMickiewicz ( forma żeńska : Mickiewicz , pot . gwar . lub przest . Mickiewiczowa ; liczba mnoga : Mickiewiczowie , pot . gwar . lub przest . Mickiewicze ) patronimiczne nazwisko polskie pochodzenia białoruskiego .\n\nOsoby o nazwisku Mickiewicz:\n\nInne:\n\n\n\n',
        "Muzeum Adama Mickiewicza w Stambule\n\nMuzeum Adama Mickiewicza w Stambule – turecka placówka muzealna , mieszcząca się w domu w Stambule , w którym 26 listopada 1855 zmarł Adam Mickiewicz .\n\nW 1955 roku , w stulecie śmierci wieszcza , otwarto tu ekspozycję . W podziemiach budynku urządzono symboliczną kryptę poety , z krzyżem i płytą nagrobną z napisem : `` Miejsce czasowego spoczynku Adama Mickiewicza , 26 listopada - 30 grudnia 1855 roku '' .\n\nOd 2005 w salach muzeum znajduje się ekspozycja przygotowana przez Muzeum Literatury im . Adama Mickiewicza w Warszawie .\n\n\n\n",
        "Józef Adam Stanisław Mickiewicz\n\nJózef Adam Stanisław Mickiewicz ( ur . 28 sierpnia 1896 r. w Warszawie , zmarł 7-go marca 1943 r. w Majdanku ) – kapitan pilot obserwator Wojska Polskiego , jeden z pionierów polskiego krótkofalarstwa – Prezes Okręgu Zachodnio Polskiego P.Z.K . 1930 r .\n\nJózef Adam Stanisław Mickiewicz był absolwentem `` Szkoły Podchorażych Piechoty '' w miejscowości Ostrów-Komorowo .\n\nZdjęcie datowane na 30 stycznia 1918 r. przedstawia go wraz z grupą kolegów podchorążych . Niektóre nazwiska można odczytać z umieszczonych na odwrocie zdjęcia pamiątkowych podpisów .\n\n\n\n",
        'Ulica Adama Mickiewicza\n\nUlica Adama Mickiewicza – popularna nazwa ulic w Polsce ;\n\nUlice:\n\nAleje:\n\nWedług TERYT w Polsce jest 354 ulic i placów Adama Mickiewicza .\n\n\n\n',
        'V Liceum Ogólnokształcące im . Adama Mickiewicza w Częstochowie\n\nV Liceum Ogólnokształcące im . Adama Mickiewicza w Częstochowie – jedna z najbardziej renomowanych i najstarszych szkół średnich w Częstochowie , potocznie określana jako Mickiewicz lub Micek , mieści się przy ulicy Krakowskiej 29 .\n\nLiceum Ogólnokształcące im . Adama Mickiewicza w Częstochowie powstało w 1949 roku , przy ulicy Kopernika w Częstochowie . Od 1954 roku do dnia dzisiejszego placówka mieści się przy ulicy Krakowskiej .\n\nW 1956 roku szkołę przekształcono na Szkołę Podstawową i Liceum Ogólnokształcące Numer 1 . Od roku 1963 funkcjonuje już samodzielnie jako liceum . W latach siedemdziesiątych XX wieku szkoła funkcjonowała jako V Liceum Ogólnokształcące im . Adama Mickiewicza .\n\n\n\n']
    query = "Adama Mickiewicz"

    word2vec = KeyedVectors.load("word2vec/word2vec_100_3_polish.bin")
    q = prep_sentence(query, word2vec)
    b = prep_sentence(bodies[0], word2vec)
    print(article_arr_score(get_sim_arr(q, b, word2vec)))
