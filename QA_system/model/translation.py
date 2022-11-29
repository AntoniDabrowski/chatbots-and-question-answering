import dl_translate as dlt
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mt = dlt.TranslationModel(device=device)

def pol_en(sentence):
    return mt.translate(sentence, source=dlt.lang.POLISH, target=dlt.lang.ENGLISH)

def en_pol(sentence):
    return mt.translate(sentence, source=dlt.lang.ENGLISH, target=dlt.lang.POLISH)

