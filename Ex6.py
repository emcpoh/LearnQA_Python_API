import requests

playground_url = "https://playground.learnqa.ru/api/long_redirect"


response = requests.get(playground_url, allow_redirects=True)

history_len = len(response.history)
final_url = response.url

print(f"Число редиректов: {history_len}")
print(f"Итоговый URL: {final_url}")