import pandas as pd
from nltk.tokenize import word_tokenize

def tokenize(corpus):
    return [' '.join(word_tokenize(sample)) for sample in corpus]

df = pd.read_csv('dev.csv')

with open('src-val.txt', 'w', encoding='UTF-8') as file:
    file.write('\n'.join(tokenize(df['src'].tolist())))

with open('tgt-val.txt', 'w', encoding='UTF-8') as file:
    file.write('\n'.join(tokenize(df['mt'].tolist())))