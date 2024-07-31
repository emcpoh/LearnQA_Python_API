import requests
from wiki_page_parser import passwords_tuple

get_secret_password_homework_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
admin_login = "super_admin"

passwords = passwords_tuple


def get_auth_cookie(user_password, user_login=admin_login):
    response = requests.post(get_secret_password_homework_url, data={"login": user_login, "password": user_password})
    auth_cookie = response.cookies.get('auth_cookie')
    return auth_cookie

def check_auth_cookie(auth_cookie):
    password_is_valid = False
    response = requests.post(check_auth_cookie_url, cookies={"auth_cookie": auth_cookie})
    if response.text == "You are NOT authorized":
        return password_is_valid, None
    elif response.text == "You are authorized":
        password_is_valid = True
        return password_is_valid, response.text
    else:
        print("ah?")


for password in passwords:
    auth_cookie = get_auth_cookie(password)
    cookie_is_valid, response_text = check_auth_cookie(auth_cookie)

    if cookie_is_valid == False:
        continue
    elif cookie_is_valid == True:
        print(f"password = {password}, response_text = {response_text}")
        break
    else:
        print("Правильных паролей в списке не оказалось")

