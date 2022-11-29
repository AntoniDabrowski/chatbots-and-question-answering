from transformers import pipeline
import dl_translate as dlt
import wikipedia as wiki
import torch
import re
import numpy as np
from tqdm.auto import tqdm
from create_query import create_query

# Translation
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mt = dlt.TranslationModel(device=device)

# Question Answering
# model_name = "deepset/roberta-base-squad2"
model_name = "deepset/minilm-uncased-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


def pol_en_translation(sentence):
    return mt.translate(sentence, source=dlt.lang.POLISH, target=dlt.lang.ENGLISH)


def wiki_ranking(question, k=5, verbose=False):
    query = create_query(question, 'en')
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
    return ranking


def QA(question, articles):
    answers = []
    for context in articles:
        QA_input = {
            'question': question,
            'context': context
        }
        answers.append(nlp(QA_input))
    return answers


def choose_ans(answers):
    scores = [answer['score'] for answer in answers]
    ans = [answer['answer'] for answer in answers]
    return ans[np.argmax(scores)]


def en_pol_translation(sentence):
    return mt.translate(sentence, source=dlt.lang.ENGLISH, target=dlt.lang.POLISH)


def pipeline(question_pl, k=5, verbose=False):
    question_en = pol_en_translation(question_pl)
    # Use deepl model to check the improvement

    if verbose:
        print(question_en)

    relevant_articles = wiki_ranking(question_en, k, verbose)
    answers = QA(question_en, relevant_articles)

    if verbose:
        for ans in answers:
            print(ans)

    answer_en = choose_ans(answers)
    answer_pl = en_pol_translation(answer_en)
    return answer_pl

def run_test():
    # Makes predictions for a whole dataset
    q = [line for line in open(r'../data/questions.txt', encoding='UTF-8')]
    answers = []
    for i, question in enumerate(tqdm(q)):
        try:
            answer = pipeline(question, k=7, verbose=False)
            print(f'{question}, {answer}')
            answers.append(answer)
        except:
            answers.append('')
        # Log results
        if i!=0 and i%100==0:
            predictions = '\n'.join(answers)+'\n'
            with open(f'../predictions/answers_query.txt', 'a', encoding='UTF-8') as file:
                file.write(predictions)
            answers = []

    # Log results after las chunk
    predictions = '\n'.join(answers) + '\n'
    with open(f'../predictions/answers_query.txt', 'a', encoding='UTF-8') as file:
        file.write(predictions)


# question = 'Jak nazywa się pierwsza litera alfabetu greckiego?'
# while True:
# print(pipeline(question, k=5, verbose=True))
    # question = input()


run_test()