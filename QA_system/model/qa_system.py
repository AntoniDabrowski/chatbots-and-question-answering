from transformers import pipeline
import dl_translate as dlt
import torch
import re
import numpy as np
from tqdm.auto import tqdm
from datetime import datetime
from get_articles import get_articles

# Translation
device = 'cuda' if torch.cuda.is_available() else 'cpu'
mt = dlt.TranslationModel(device=device)

# Question Answering
# model_name = "deepset/roberta-base-squad2"
model_name = "deepset/minilm-uncased-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)


def pol_en_translation(sentence):
    return mt.translate(sentence, source=dlt.lang.POLISH, target=dlt.lang.ENGLISH)

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

    relevant_articles = get_articles(question_en, k, verbose)
    answers = QA(question_en, relevant_articles)

    if verbose:
        for ans in answers:
            print(ans)

    answer_en = choose_ans(answers)
    answer_pl = en_pol_translation(answer_en)
    return answer_pl

def run_test():
    # Makes predictions for a whole dataset
    q = [line for line in open(r'../data/questions.txt',encoding='UTF-8')]
    answers = []
    for question in tqdm(q):
        try:
            answer = pipeline(question,k=7,verbose=False)
            print(f'{question}, {answer}')
            answers.append(answer)
        except:
            answers.append('')

    predictions = '\n'.join(answers)
    time = datetime.now().strftime("%d_%m_%Y__%H_%M")
    with open(f'../predictions/answers_{time}.txt','w',encoding='UTF-8') as file:
        file.write(predictions)


question = 'Jak nazywa się pierwsza litera alfabetu greckiego?'
# while True:
print(pipeline(question, k=5, verbose=True))
    # question = input()


# run_test()
