import asyncio
import requests
import json

from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey
from add_analysis_funcs import *

def make_advice(short_text):
    conf = read_config("/Users/dmitryderyugin/startups/ADNews/ADNewsSite/src/adnews/analysis/config/config.yaml")    
    text = get_advice_prompt(summ=short_text)

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
                "text": text
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

    print(text)
    print("\n")

    advice = result["result"]["alternatives"][0]["message"]["text"]

    return advice

# have to do something with list of equities