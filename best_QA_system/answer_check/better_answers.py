from advent_answer_check import check_answers

found_answers = []
correct_answers = []
questions = [q.rstrip() for q in open('../data/questions_A_prime.txt','r',encoding='UTF-8')]

century = {"XIX":'19'}
def contain_century(answer):
    for k,v in century.items():
        if k.lower() in answer:
            return v
    return False

num = {'jeden':'1','dwa':'2','trzy':'3','cztery':'4','pięć':'5','sześć':'6','siedem':'7','osiem':'8','dziewięć':'9'}
def contain_number(answer):
    for k,v in num.items():
        if k in answer:
            return v
    return False


for x in open('../data/answers_A_prime.txt', encoding='UTF-8'):
    x = x.strip()
    correct_answers.append(x.lower().split('\t'))

for x in open('../predictions/answers_A_prime_EN.txt', encoding='UTF-8'):
    x = x.strip()
    found_answers.append(x.lower())

def change_answers(questions,found_answers):
    new_answers = []
    # 38.7%
    for question, answer in zip(questions,found_answers):
        if 'tak' in answer.lower():
            new_answers.append('tak')
        elif 'nie' in answer.lower():
            new_answers.append('nie')
        # 39.7%
        elif 'jak' in question.lower() and 'imię' in question.lower() and answer:
            new_answers.append(answer.split()[0])
        # 40.7%
        elif '.' in answer:
            new_answers.append(answer.replace('.',''))
        # 41.4%
        elif contain_number(answer):
            new_answers.append(contain_number(answer))
        # 42%
        elif contain_century(answer):
            new_answers.append(contain_century(answer))
        elif 'W którym mieście' in question:
            new_answers.append(answer.split(',')[0])
        # 42.57%
        else:
            new_answers.append(answer)
    with open('../predictions/answers_A_prime_EN_h.txt','w',encoding="UTF-8") as file:
        file.write('\n'.join(new_answers))
    print(check_answers(correct_answers,new_answers))

change_answers(questions,found_answers)