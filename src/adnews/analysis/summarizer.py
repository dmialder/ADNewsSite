import asyncio
import requests
import json

from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey
from add_analysis_funcs import *

def YGPT_analysis(news_text, prompt_text):
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")    

    prompt = {
        "modelUri": f"gpt://{conf['GPT_access']['identity']}/{conf['GPT_access']['model']}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 100
        },
        "messages": [
            {
                "role": "user",
                "text": prompt_text
            }
        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {conf['GPT_access']['key']}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()

    summarization = result["result"]["alternatives"][0]["message"]["text"]

    return summarization


def try_1():
    text = """Благодушие при подготовке к отопительному сезону неуместно, заявил президент Владимир Путин на совещании с членами правительства.«Благодушие здесь точно неуместно, все, о чем вы говорили, надо жестко проводить в жизнь», — сказал он после доклада главы Минэнерго Сергея Цивилева, согласно которому все выглядит «своевременно и складно». В докладе министр подчеркнул, что энергосистема страны готова к прохождению пиковых зимних максимумов. Путин также пообещал рассказать Цивилеву, как Виктор Черномырдин, будучи председателем правительства, рекомендовал Минэнерго готовиться к осенне-зимнему периоду."""

    summ = YGPT_analysis(text, prompt_text)
    print(summ)


def try_2():
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")
    print(conf)
    print(conf["GPT_access"]["identity"])
    print(conf["GPT_access"]["key"])


if __name__ == "__main__":
    try_1()