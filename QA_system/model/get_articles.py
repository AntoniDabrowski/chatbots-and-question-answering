import re
import wikipedia as wiki
from create_query import create_query
import translation

def get_articles(question_pl, k=5, verbose=False):
    question_en = translation.pol_en(question_pl)
    # Use deepl model to check the improvement

    if verbose:
        print(question_en)

    query = create_query(question_en, 'en')
    results = wiki.search(query)
    ranking = []
    for i in range(min(k, len(results))):
        try:
            if verbose:
                print(i + 1, results[i])
            article = wiki.page(results[i]).content

            # preprocessing: wikipedia contain many specific information in brackets
            # those were mostly useless for QA and model behave strangely on them
            # therefore I removed them
            article = re.sub("\(.*?\)", "", article)
            if verbose:
                print(article[:200])

            ranking.append(article[:1000])
        except:
            if verbose:
                print("No matching article")
    return [ranking, question_en]

