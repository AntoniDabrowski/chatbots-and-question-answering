from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.nist_score import sentence_nist
from nltk.translate.meteor_score import single_meteor_score
from tqdm.auto import tqdm
import numpy as np
import matplotlib.pyplot as plt


def single_score(reference, hypothesis):
    return sentence_bleu([reference], hypothesis), \
           sentence_nist([reference], hypothesis), \
           single_meteor_score(reference.split(), hypothesis.split())


ground_truth = [line for line in open('ground_truth.txt', encoding="UTF-8")]
pred_25000 = [line for line in open('pred_25000.txt', encoding="UTF-8")]
pred_hf = [line for line in open('pred_hf.txt', encoding="UTF-8")]
deepL = [line for line in open('deepL.txt', encoding="UTF-8")]
google_translate = [line for line in open('google_translate.txt', encoding="UTF-8")]


def compare(hypothesis):
    bleu = []
    nist = []
    meteor = []
    for h, r in tqdm(zip(hypothesis, ground_truth)):
        s1, s2, s3 = single_score(r, h)
        bleu.append(s1)
        nist.append(s2)
        meteor.append(s3)
    return np.mean(bleu), np.mean(nist), np.mean(meteor)


a = compare(deepL)
b = compare(google_translate)
c = compare(pred_hf)
d = compare(pred_25000)

data = [a, b, c, d]
X = np.arange(3)
fig = plt.figure(figsize=(10, 6))

plt.bar(X + 0.0, data[0], color='b', width=0.2, label='DeepL')
plt.bar(X + 0.2, data[1], color='g', width=0.2, label='Google Translate')
plt.bar(X + 0.4, data[2], color='r', width=0.2, label='Hugging Face')
plt.bar(X + 0.6, data[3], color='k', width=0.2, label='OpenNMT')

plt.xlabel('Translation metric', fontweight='bold', fontsize=15)
plt.ylabel('Score', fontweight='bold', fontsize=15)
plt.xticks([0.0, 1.0, 2.0], ['BLEU', 'NIST', 'METEOR'])

plt.legend()
plt.show()
