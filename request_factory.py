import http.client
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import openai


def get_image(query: str) -> str:
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
      "q": f"{query}",
      "gl": "us",
      "hl": "en",
      "autocorrect": True
    })
    headers = {
        'X-API-KEY': '9906dcefde342b975a8ee16a3f1fc1c92a1d5ede',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/images", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = data.decode("utf-8")
    result = result.replace('null','None')
    result = result.replace('true','True')
    result = result.replace('false','False')
    link = eval(result)
    link = link['images']
    return link[0]['imageUrl']

def translate(query: str) -> str:
    #resp = requests.get(f"https://translate.google.com/?sl=ru&tl=en&text={query}&op=translate")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    dr = driver.get(f"https://translate.google.com/?sl=ru&tl=en&text={query}&op=translate")
    time.sleep(3)
    trans = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[8]/div/div[1]/span[1]/span/span')
    return trans.text

def gtp(query: str) -> any:
    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{query}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response['choices'][0]['text']


