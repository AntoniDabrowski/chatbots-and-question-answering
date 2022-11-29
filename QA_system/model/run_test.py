from qa_system import answer_questions
from datetime import datetime
from check_answers import check_answers

#question = 'Jak nazywa się pierwsza litera alfabetu greckiego?'
# while True:
# print(pipeline(question, k=5, verbose=True))
    # question = input()

# Makes predictions for a whole dataset
q = [line for line in open(r'../data/questions.txt',encoding='UTF-8')][:1]
answers = answer_questions(q)

predictions = '\n'.join(answers)
time = datetime.now().strftime("%d_%m_%Y__%H_%M")
with open(f'../predictions/answers_{time}.txt','w',encoding='UTF-8') as file:
    file.write(predictions)
    file.close()
    check_answers(f'../predictions/answers_{time}.txt')
