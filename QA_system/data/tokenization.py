import spacy
from tqdm.auto import tqdm

nlp = spacy.load("pl_core_news_sm")
data = [line for line in open(r'questions.txt',encoding='utf-8')]

with open(r'questions_tokenized.txt','w',encoding='utf-8') as file:
    for sentence in tqdm(data):
        doc = nlp(sentence)
        file.write(' '.join(token.text.lower() for token in doc))