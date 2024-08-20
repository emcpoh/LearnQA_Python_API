import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


create_user_url = 'https://playground.learnqa.ru/api/user'

class TestUserRegister(BaseCase):
    def test_create_user(self):
        data = self.prepare_registration_data()

        response = requests.post(create_user_url, data=data)
        
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post(create_user_url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"