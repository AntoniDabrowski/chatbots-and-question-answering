import json

# install deepl package: pip install --upgrade deepl
import deepl

#  Replace with your key
API_KEY = "4499603e-81e6-55fd-00d1-a7913b6765df:fx"
# Modify the file path
FILE_PATH = "data/segment_0.json"


def translate_conversation(translator, conv):
    translated_conv = []

    for sentence in conv:
        try:
            result = translator.translate_text(sentence, target_lang="pl")
            translated_conv.append(result.text)
        except Exception as e:
            print(e)
            return

    return translated_conv


def translate(conversations):
    translator = deepl.Translator(API_KEY)
    translated = []

    for conv in conversations:
        translated_conv = translate_conversation(translator, conv)

        if translated_conv:
            translated.append(translated_conv)

    return translated


if __name__ == "__main__":
    with open(FILE_PATH, 'r') as file:
        to_translate = json.load(file)

    translated = translate(to_translate)

    # Modify the outfile name
    with open('polish_segment_0.json', 'w') as file:
        json.dump(translated, file)
