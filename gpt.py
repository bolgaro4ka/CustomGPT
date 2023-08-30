import openai
import requests
import voice

apis=open('keys.apikey').read().split(', ')
openai.api_key = apis[0]
messages = []

def validetor(question):
    question=question.split(' ')
    print(question)
    if ('погода' in question) or ('погоде' in question) or ('погоду' in question) or ('погодка' in question) or ('Погода' in question):
        try:
            params = {'q': 'Novodugino,RU', 'units': 'metric', 'lang': 'ru',
                      'appid': apis[1]}
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            if not response:
                raise
            w = response.json()
            return (f" На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

        except:
            return (' Произошла ошибка при попытке запроса к ресурсу API, проверь код')
    elif ('заглушка' in question) or ('Заглушка' in question):
        return 'Эта фраза является заглушкой, для того чтобы проверить программу не задействуя ЧатДжиБиТи! В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров.'
    elif ([''] == question) or ([' ']==question): return 'Пустой запрос!'
    else: return 'OMG'

def answer(question, temperature):
    valid=validetor(question)
    print(valid)
    if valid == "OMG":
        message = question  # вводим сообщение
        if message == "quit": return 7


        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=temperature)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
    else: return valid
