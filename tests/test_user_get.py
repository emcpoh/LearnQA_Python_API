import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

get_user_url = 'https://playground.learnqa.ru/api/user/'
login_url = 'https://playground.learnqa.ru/api/user/login'
class TestUserGet(BaseCase):
    def test_get_user_details_no_auth(self):
        response = requests.get(f'{get_user_url}2')
        print(response)
        Assertions.assert_json_has_keys(response, 'username')
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        login_response = requests.post(login_url, data=data)
        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(login_response, 'user_id')

        auth_response = requests.get(f'{get_user_url}{user_id_from_auth_method}',
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})
        
        Assertions.assert_json_has_keys(auth_response, 'username', 'email', 'firstName', 'lastName')
        # Assertions.assert_json_has_key(auth_response, 'email')
        # Assertions.assert_json_has_key(auth_response, 'firstName')
        # Assertions.assert_json_has_key(auth_response, 'lastName')