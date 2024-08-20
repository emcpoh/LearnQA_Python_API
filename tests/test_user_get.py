import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('Get user cases')
class TestUserGet(BaseCase):

    @allure.description('This test get user details withoun auth')
    def test_get_user_details_no_auth(self):
        response = MyRequests.get(f'{MyRequests.user_registration_uri}/2') # Хардкодим id = 2 для существующего пользователя
        
        Assertions.assert_json_has_keys(response, 'username')
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')

    @allure.description('This test get user details while being authorized as the same user')
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        login_response = MyRequests.post(MyRequests.user_login_uri, data=data)
        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(login_response, 'user_id')

        auth_response = MyRequests.get(f'{MyRequests.user_registration_uri}/{user_id_from_auth_method}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid})
        
        Assertions.assert_json_has_keys(auth_response, 'username', 'email', 'firstName', 'lastName')