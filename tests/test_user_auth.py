import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

login_url = 'https://playground.learnqa.ru/api/user/login'
auth_url = 'https://playground.learnqa.ru/api/user/auth'

class TestUserAuth(BaseCase):
    exclude_params = {
        ('no_cookie'),
        ('no_token')
    }
        
    def setup_method(self):
        
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        login_response = requests.post(login_url, data=self.data)

        self.auth_sid = self.get_cookie(login_response, 'auth_sid')
        self.token = self.get_header(login_response, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(login_response, 'user_id')
        self.headers = {'x-csrf-token': self.token}
        self.cookies = {'auth_sid': self.auth_sid}
        
    def test_auth_user(self):

        response = requests.get(auth_url, headers=self.headers, cookies=self.cookies)

        Assertions.assert_json_value_by_name(
            response,
            'user_id',
            self.user_id_from_auth_method,
            'User id from auth method is not equal to user id from check method'
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_token':
            response = requests.get(auth_url, headers=self.headers)
        elif condition == 'no_cookie':
            response = requests.get(auth_url, cookies=self.cookies)
        else:
            print(f'Unknown condition : {condition}')

        Assertions.assert_json_value_by_name(
            response,
            'user_id',
            0,
            f'User is authorized with condition {condition}'
        )

