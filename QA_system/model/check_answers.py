import editdistance
from tqdm.auto import tqdm

def scaled_editdist(ans, cor):
    ans = ans.lower()
    cor = cor.lower()

    return editdistance.eval(ans, cor) / len(cor)

def single_match(a, c):
    if c.isdecimal():
        return a == c
    return scaled_editdist(a, c) < 0.5


def match(ans, cor):
    return any(single_match(ans, c) for c in cor)

def check_answers(answers_filename):
    found_answers = []
    correct_answers = []

    for x in open('../data/correct_answers.txt', encoding='UTF-8'):
        x = x.strip()
        correct_answers.append(x.lower().split('\t'))

    for x in open(answers_filename, encoding='UTF-8'):
        x = x.strip()
        found_answers.append(x.lower())

    N = len(correct_answers)
    score = 0.0
    matched_id = []
    for i, (ans, cor) in tqdm(enumerate(zip(found_answers, correct_answers))):
        if match(ans, cor):
            score += 1
            matched_id.append(i)

    print('TOTAL SCORE:', f'{score/35}%')
    # print('Good answered questions:')
    # print(repr(matched_id))
