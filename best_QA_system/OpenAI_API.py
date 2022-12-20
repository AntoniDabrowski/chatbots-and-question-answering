import openai

# https://beta.openai.com/account/usage
openai.api_key = "INSERT-HERE-YOUR-KEY"


def QA(question, prompt=lambda q: f"Q: {q}\nA: "):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt(question),
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return response['choices'][0]['text']


def test_run():
    while True:
        question = input()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {question}\nA: ",
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        print(response)

# test_run()
# Were deputies and messengers appointed in ancient states?
