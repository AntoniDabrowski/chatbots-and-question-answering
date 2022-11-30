import re
import wikipedia as wiki
from create_query import create_query
from datetime import datetime
import translation

def get_articles_titles(question, results, language):
    wiki.set_lang(language)
    return wiki.search(question, results=results)

def get_articles(question_pl, k=5, verbose=False):
    # t = datetime.now()
    question_en = translation.pol_en(question_pl)
    # Use deepl model to check the improvement

    if verbose:
        print(question_en)
    
    query_pl = create_query(question_pl, 'pl')
    query_en = create_query(question_en, 'en')
    titles = get_articles_titles(query_en, k, 'en')
    titles_using_polish_query = []

    for title_pl in get_articles_titles(query_pl, 1, 'pl'):
        title_en = translation.pol_en(title_pl)
        for possible_title_en in get_articles_titles(title_en, int(k / 3), 'en'):
            titles_using_polish_query.append(possible_title_en)
            
    # print("get articles titles time =", datetime.now() - t)
    # t = datetime.now()

    while len(titles) + len(titles_using_polish_query) > k:
        if len(titles) > len(titles_using_polish_query):
            titles = titles[:-1]
        else:
            titles_using_polish_query = titles_using_polish_query[:-1]
            
    titles = titles + titles_using_polish_query
    ranking = []
    assert(len(titles) <= k)
    for i in range(len(titles)):
        try:
            if verbose:
                print(i + 1, titles[i])
            article = re.sub("\(.*?\)", "", wiki.page(titles[i]).content)

            # preprocessing: wikipedia contain many specific information in brackets
            # those were mostly useless for QA and model behave strangely on them
            # therefore I removed them
            if verbose:
                print(article[:200])

            ranking.append(article[:1000])
        except:
            if verbose:
                print("No matching article")
    # print("get_articles context time =", datetime.now() - t)
    return [ranking, question_en]

