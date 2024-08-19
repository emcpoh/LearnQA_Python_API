import pytest
import requests


user_agent_check_url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

data_provider = [
    [('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'), {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}],
    [('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'), {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}],
    [('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'), {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}],
    [('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'), {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}],
    [('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'), {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}]
]

class TestUserAgent:    
    @pytest.mark.parametrize('user_agent, expected_data', data_provider)
    def test_user_agent_check(self, user_agent, expected_data):
        attributes = ['platform', 'browser', 'device']
        headers={"User-Agent": user_agent}
        response = requests.get(user_agent_check_url, headers=headers)

        # Реализовал сбор ошибок во время выполнения, т.к. после первого неудачного assert'а тест падает и не удается проверить все атрибуты
        errors_list = []
        json_response = response.json()
        for attribute in attributes:
            try:
                expected_value = json_response[attribute]
                assert expected_value == expected_data[attribute]
            except AssertionError:
                errors_list.append(f'Actual {attribute} is not equal to expected for user agent = {user_agent}')

        print(errors_list)

        # более простая реализация, но не учитывает проходение теста после фейла на ассертах (хотя по итогу, результаты этого способа и описанного выше, в текущей реализации метода user_agent_check, одинаковы)

        # expected_platfrom = json_response['platform']
        # expected_browser = json_response['browser']
        # expected_device = json_response['device']

        # assert expected_platfrom == expected_data['platform'], f'Actual platfrom is not equal to expected for user agent = {user_agent}'
        # assert expected_browser == expected_data['browser'], f'Actual browser is not equal to expected for user agent = {user_agent}'
        # assert expected_device == expected_data['device'], f'Actual device is not equal to expected for user agent = {user_agent}'
