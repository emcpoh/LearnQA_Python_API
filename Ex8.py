import time
import json
import requests

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

seconds_key = "seconds"
token_key = "token"

# создаем задачу
task_creation = requests.get(url)

# парсим ответ
response_json = task_creation.json()
token = response_json[token_key]
time_to_sleep = response_json[seconds_key]
print(f"Token = {token}, time_to_sleep = {time_to_sleep}")

# запрос с token
response_from_request_with_token = requests.get(url, params={"token": token})

# парсим убеждемся в правильности поля status
json_from_request_with_token = response_from_request_with_token.json()
print(json_from_request_with_token)
assert json_from_request_with_token["status"] == "Job is NOT ready"

# спим до готовности задачи
time.sleep(time_to_sleep)

# запрос с token
response_after_sleep = requests.get(url, params={"token": token})

# парсим и убеждаемся в правильности поля status и наличии поля result

json_after_finish = response_after_sleep.json()
print(json_after_finish)
assert json_after_finish["status"] == "Job is ready"
assert json_after_finish["result"] is not None

print("Script executed successfully!")