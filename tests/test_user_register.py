import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('Test user registration cases')
class TestUserRegister(BaseCase):

    @allure.description('This test create new user')
    def test_create_user(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(MyRequests.user_registration_uri, data=data)
        
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, 'id')

    @allure.description('This test create user with existing email')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(MyRequests.user_registration_uri, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"