import morfeusz2
import pickle
import colorama
from termcolor import colored
import numpy as np
from gensim.models import KeyedVectors
from sparse_retriever import get_ranking, print_result
from time import time
from dense_retriever import article_score
from tqdm import tqdm


if __name__ == '__main__':
    # Initialization
    t_previous = time()
    print(f'Loading models and databases...\nExecution time: 0.0s')
    morf = morfeusz2.Morfeusz()
    colorama.init(autoreset=True)
    w2v = KeyedVectors.load("word2vec/word2vec_100_3_polish.bin")

    path = r"C:\Users\user\Studia\Semestr VI\Eksploracja tekstów\Text_mining\dane\wikipedyjka"
    titles = pickle.load(open(path+r'\id_titles.pickle',"rb"))
    body = pickle.load(open(path+r'\id_body.pickle', "rb"))
    odwrotny_indeks_titles = pickle.load(open(path+r'\odwrotny_indeks_titles.pickle',"rb"))
    odwrotny_indeks_body = pickle.load(open(path+r'\odwrotny_indeks_body.pickle',"rb"))
    odwrotny_indeks_lematyczny_titles = pickle.load(open(path+r'\odwrotny_indeks_lematyczny_titles.pickle',"rb"))
    odwrotny_indeks_lematyczny_body = pickle.load(open(path+r'\odwrotny_indeks_lematyczny_body.pickle',"rb"))

    data = (odwrotny_indeks_titles, odwrotny_indeks_body,
            odwrotny_indeks_lematyczny_titles, odwrotny_indeks_lematyczny_body, body, morf)
    combinations = []
    for a in range(9,0,-1):
        for b in range(9,0,-1):
            for c in range(9,0,-1):
                for d in range(9,0,-1):
                    combinations.append([a,b,c,d])

    for a,b,c,d in tqdm(combinations):
        # print(f'Permutation: {a}, {b}, {c}, {d}')
        matches_importance = {'match_in_title': a,
                              'lemma_match_in_title': b,
                              'match_in_body': c,
                              'lemma_match_in_body': d}

        # QA loop
        verbose = False
        k = 5
        # print(f"Done! You can ask questions!\nExecution time:{(time()-t_previous):.2f}s")
        questions = [question for question in open('data/questions.txt',encoding='utf-8')]

        answers = []
        top_answers = []

        for query in questions:

            if verbose:
                print(query)
                # Logging time
                t_previous = time()


            ranking, matches = get_ranking(query, data, matches_importance, log_matches=True)

            # choosing best five results
            sorted_results = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
            if verbose:
                for article_id, relevance in sorted_results[:k]:
                    # if relevance > 0.6:
                    print_result(article_id, titles, body, relevance, matches, morf)
                print("Matching:" +
                      colored('\nPERFECT MATCH IN TITLE', 'red') +
                      colored('\nLEMMA MATCH IN TITLE', 'magenta') +
                      colored('\nPERFECT MATCH IN ARTICLE BODY', 'blue') +
                      colored('\nLEMMA MATCH IN ARTICLE BODY', 'yellow'))
                print(f'Execution time: {time()-t_previous}s')

            bodies = [body[article_id] for article_id, _ in sorted_results[:k]]

            sparse_scores = np.array([score for _, score in sorted_results[:k]])
            dense_scores = np.array([article_score(b, query, w2v) for b in bodies])

            final_score = sparse_scores * dense_scores
            winning_id, _ = sorted_results[np.argmax(final_score)]

            if verbose:
                print(titles[winning_id])

            answers.append(titles[winning_id].rstrip())
            top_answers.append([titles[top_id].rstrip() for top_id, _ in sorted_results[:k]])


        with open(f'predictions/answers_{a}{b}{c}{d}.txt','w',encoding='utf-8') as file:
            file.write('\n'.join(answers))

        # with open('predictions/top_k_answers_{a}{b}{c}{d}.txt','w',encoding='utf-8') as file:
        #     file.write('\n'.join([','.join(one_line) for one_line in top_answers]))
