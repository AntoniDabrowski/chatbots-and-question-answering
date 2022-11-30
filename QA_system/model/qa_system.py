from transformers import pipeline
import re
import numpy as np
from tqdm.auto import tqdm
from datetime import datetime
import translation
from get_articles import get_articles


# Question Answering
# model_name = "deepset/roberta-base-squad2"
model_name = "deepset/minilm-uncased-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def QA(question, articles):
    answers = []
    # t = datetime.now()
    for context in articles:
        QA_input = {
            'question': question,
            'context': context
        }
        answers.append(nlp(QA_input))
    # print("QA time =", datetime.now() - t)
    return answers

def choose_ans(answers):
    if len(answers) == 0:
        return ''
    scores = [answer['score'] for answer in answers]
    ans = [answer['answer'] for answer in answers]
    return ans[np.argmax(scores)]

def pipeline(question_pl, k=5, verbose=False):
    [relevant_articles, question_en] = get_articles(question_pl, k, verbose)
    answers = QA(question_en, relevant_articles)

    if verbose:
        for ans in answers:
            print(ans)

    answer_en = choose_ans(answers)
    answer_pl = translation.en_pol(answer_en)
    return answer_pl

def answer_questions(questions, verbose, verbose_pipeline):
    answers = []
    for question in tqdm(questions):
        try:
            answer = pipeline(question,k=12,verbose=verbose_pipeline)
            if verbose:
                print(f'{question}, {answer}')
            answers.append(answer)
        except:
            answers.append('')
    return answers

