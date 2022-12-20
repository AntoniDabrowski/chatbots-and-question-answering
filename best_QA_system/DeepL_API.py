import deepl
from tqdm import tqdm

# https://www.deepl.com/account/usage
auth_key = 'INSERT-HERE-YOUR-KEY'
translator = deepl.Translator(auth_key)


def translate(question,lang):
    return translator.translate_text(question, target_lang=lang).text


def run_DeepL():
    while True:
        text = input()
        result = translator.translate_text(text, target_lang="EN-GB")
        translated_text = result.text
        print(translated_text)

# run_DeepL()

# questions_PL = [question.rstrip() for question in open('./data/questions_A.txt', 'r', encoding='UTF-8')]
# questions_EN = [translate(question_PL.rstrip(),lang='EN-GB') for question_PL in tqdm(questions_PL)]
#
# with open(f'./data/questions_A_EN.txt.txt', 'w', encoding='UTF-8') as file:
#     file.write('\n'.join(questions_EN))