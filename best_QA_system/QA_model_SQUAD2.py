from transformers import pipeline

model_name = "deepset/minilm-uncased-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def QA_SQUAD(question,context):
    QA_input = {
        'question': question,
        'context': context
    }
    return nlp(QA_input)