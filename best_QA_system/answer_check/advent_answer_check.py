import editdistance
import sys

rn = ['ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii',
      'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii']

rome_numbers = dict(zip(rn, range(2, 23)))


def numbers_from(s):
    res = set()
    for w in s.split():
        w = w.lower()
        if w.isdecimal():
            res.add(w)
        if w in rome_numbers:
            res.add(rome_numbers[w])
    return res


# def is_number(s):
#     return lower(s) in rome_numbers or s.isdecimal()

def scaled_editdist(ans, cor):
    ans = ans.lower()
    cor = cor.lower()

    return editdistance.eval(ans, cor) / len(cor)


def single_match(a, c):
    numbers_c = numbers_from(c)
    numbers_a = numbers_from(a)

    return numbers_a == numbers_c and scaled_editdist(a, c) < 0.5


def match(ans, cor):
    return any(single_match(ans, c) for c in cor)


def check_answers(correct_answers, found_answers):
    N = len(correct_answers)
    score = 0.0

    good_ids = []
    bad_ids = []

    for i, (ans, cor) in enumerate(zip(found_answers, correct_answers)):
        if match(ans, cor):
            score += 1
            good_ids.append(i)
        else:
            bad_ids.append(i)

    # print(repr(good_ids))
    # print(repr(bad_ids))
    return f'TOTAL SCORE: {score / N}'


def run():
    correct_answers = []
    found_answers = []

    for x in open('../data/answers_A_prime.txt', encoding='UTF-8'):
        x = x.strip()
        correct_answers.append(x.lower().split('\t'))

    for x in open('../predictions/answers_A_prime_EN_h.txt', encoding='UTF-8'):
        x = x.strip()
        found_answers.append(x.lower())

    print(check_answers(correct_answers, found_answers))
