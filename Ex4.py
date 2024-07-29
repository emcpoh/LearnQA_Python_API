import requests

playground_url = 'https://playground.learnqa.ru/api/get_text'

response = requests.get(playground_url).text
print(response)