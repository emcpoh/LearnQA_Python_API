import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

login_endpoint = '/user/login'
auth_endpoint = '/user/auth'

@allure.epic('Authorization cases')
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
        login_response = MyRequests.post(login_endpoint, data=self.data)

        self.auth_sid = self.get_cookie(login_response, 'auth_sid')
        self.token = self.get_header(login_response, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(login_response, 'user_id')
        self.headers = {'x-csrf-token': self.token}
        self.cookies = {'auth_sid': self.auth_sid}

    @allure.description('This test successfuly authorize user by email and password')    
    def test_auth_user(self):
        
        response = MyRequests.get(auth_endpoint, headers=self.headers, cookies=self.cookies)

        Assertions.assert_json_value_by_name(
            response,
            'user_id',
            self.user_id_from_auth_method,
            'User id from auth method is not equal to user id from check method'
        )
    
    @allure.description('This test check authorization status w/o cookies or token')
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == 'no_token':
            response = MyRequests.get(auth_endpoint, headers=self.headers)
        elif condition == 'no_cookie':
            response = MyRequests.get(auth_endpoint, cookies=self.cookies)
        else:
            print(f'Unknown condition : {condition}')

        Assertions.assert_json_value_by_name(
            response,
            'user_id',
            0,
            f'User is authorized with condition {condition}'
        )

