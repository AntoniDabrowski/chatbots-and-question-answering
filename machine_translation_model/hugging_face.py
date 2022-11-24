import dl_translate as dlt

mt = dlt.TranslationModel(device='cpu')

sentence = "All branches of these structures can be hidden before the publication on the site ."

with open('results/pred_hf.txt','a',encoding='UTF-8') as file:
    file.write(mt.translate(sentence, source=dlt.lang.ENGLISH, target=dlt.lang.POLISH))
