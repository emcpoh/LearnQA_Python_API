import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

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
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    # - Создание пользователя с некорректным email - без символа @
    email = [
        'test',
        'test.ru',
        '123@',
        '  test@testexample.com  ',
        '@.ru'
        ]
    @allure.description('This test tries to create a user with invalid email')
    @pytest.mark.parametrize('email', email)
    def test_create_user_with_invalid_email(self, email):
        data = self.prepare_registration_data(email)

        response = MyRequests.post(MyRequests.user_registration_uri, data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"Invalid email format")

    missed_param = [
        'username',
        'firstName',
        'lastName',
        'email',
        'password'
    ]
    @allure.description('This test tries to create a user w/o one of param')
    @pytest.mark.parametrize('missed_param', missed_param)
    def test_create_user_without_param(self, missed_param):
        data = self.prepare_registration_data()
        data.pop(missed_param)

        response = MyRequests.post(MyRequests.user_registration_uri, data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f'The following required params are missed: {missed_param}')

    changed_username_cases = [
        ['A', 400, "The value of 'username' field is too short"],
        ['', 400, "The value of 'username' field is too short"],
        [f"{'A' * 251}", 400, "The value of 'username' field is too long"],
        ['valid username', 200, None]
        ]
    @allure.description('This test tries to create a user with changed username')
    @pytest.mark.parametrize('changed_username, expected_status_code, expected_description', changed_username_cases)
    def test_create_user_with_changed_username(self, changed_username, expected_status_code, expected_description):
        data = self.prepare_registration_data(username=changed_username)

        response = MyRequests.post(MyRequests.user_registration_uri, data=data)

        Assertions.assert_code_status(response, expected_status_code)
        Assertions.assert_content(response, expected_description)