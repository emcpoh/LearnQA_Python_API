import requests
from requests import Response

homework_cookie_url = 'https://playground.learnqa.ru/api/homework_cookie'


class TestHomeworkCookie:
    def test_homework_cookie(self):
        expected_cookie_name = 'HomeWork'
        expected_cookie_values = 'hw_value'
        response = requests.get(homework_cookie_url)

        for cookie in response.cookies:
            print(f'cookie_name = {cookie.name}, cookie_value: {cookie.value}')
            actual_cookie_name = cookie.name
            actual_cookie_value = cookie.value

        assert actual_cookie_name == expected_cookie_name, f'Actual cookie name is not equal to {expected_cookie_name}'
        assert actual_cookie_value == expected_cookie_values, f'Actual cookie value is not equal to {expected_cookie_values}'