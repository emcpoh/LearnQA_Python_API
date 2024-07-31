import requests

playgroud_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

used_methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

# 1. Делаем http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response_1 = requests.get(playgroud_url)
# В результате выполнения запроса возвращается 200 статус-код и текст 'Wrong method provided'.
# Ожидаемое поведение - вернулся 200 статус-код и объект {"success":"!"}


# 2. Делаем http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response_2 = requests.head(playgroud_url, data={"method": "HEAD"})
# В результате выполнения запроса возвращается 400 статус-код, хотя метод и параметр совпадают


# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response_3 = requests.post(playgroud_url, data={"method": used_methods[1]})
# В результате выполнения запроса возвращается 200 статус-код и объект {"success":"!"}


success_status_code = 200
bad_request_status_code = 400

wrong_methods_but_success = []
correct_method_but_bad_request = []
# 4. Перебор методов
for real_method in used_methods:
    for param_method in used_methods:
        if real_method == "GET":
            response = requests.get(playgroud_url, params={"method": param_method})
        elif real_method == "POST":
            response = requests.post(playgroud_url, data={"method": param_method})
        elif real_method == "PUT":
            response = requests.put(playgroud_url, data={"method": param_method})
        elif real_method == "DELETE":
            response = requests.delete(playgroud_url, data={"method": param_method})
        
        if real_method == param_method and (response.status_code != success_status_code or response.text != '{"success":"!"}'):
            correct_method_but_bad_request.append((real_method, param_method, response.status_code, response.text))
        elif real_method != param_method and response.status_code == success_status_code and response.text == '{"success":"!"}':
            wrong_methods_but_success.append((real_method, param_method, response.status_code, response.text))

# Вывод результатов
print("Сочетания, когда реальный метод совпадает с параметром, но сервер отвечает некорректно:")
for method in correct_method_but_bad_request:
    print(f"Реальный метод: {method[0]}, Параметр method: {method[1]}, Статус код: {method[2]}, Ответ: {method[3]}")

print("Сочетания, когда реальный метод не совпадает с параметром, но сервер отвечает корректно:")
for method in wrong_methods_but_success:
    print(f"Реальный метод: {method[0]}, Параметр method: {method[1]}, Статус код: {method[2]}, Ответ: {method[3]}")