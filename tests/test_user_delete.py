import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('Test user deletion cases')
class TestUserDelete(BaseCase):
    @allure.description('This test tries to delete test user with id = 2')
    def test_delete_test_user(self):
        email = 'vinkotov@example.com'
        password = '1234'
        user_id = '2'

        headers, cookies = self.login_as_user(email, password)

        response = MyRequests.delete(f'{MyRequests.user_registration_uri}/{user_id}', 
                                     headers=headers,
                                     cookies=cookies)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, 'error', 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.',
                                             f'Unexpected response: {response.content}')
        
    @allure.description('This test delete a new user')
    def test_delete_new_user(self):
        with allure.step('Delete a new registered user'):
            email, password, user_id = self.register_user()
            headers, cookies = self.login_as_user(email, password)

            user_delete_response = MyRequests.delete(f'{MyRequests.user_registration_uri}/{user_id}', 
                                        headers=headers,
                                        cookies=cookies)
            
            Assertions.assert_code_status(user_delete_response, 200)
            Assertions.assert_json_value_by_name(user_delete_response, 'success', '!', 'Error while user deletion')

        with allure.step('Try to get a deleted user'):
            response = MyRequests.get(f'{MyRequests.user_registration_uri}/{user_id}', 
                                        headers=headers,
                                        cookies=cookies)
            
            Assertions.assert_code_status(response, 404)
            Assertions.assert_content(response, 'User not found')

    @allure.description('This test tries to delete user being auth as different user')
    def test_delete_user_auth_diff_user(self):
            with allure.step('First user registration and login'):
                first_user_email, first_user_password, first_user_id = self.register_user()
                first_user_headers, first_user_cookies = self.login_as_user(first_user_email, first_user_password)

            with allure.step('Second user registration and login'):
                second_user_email, second_user_password, second_user_id = self.register_user()

            with allure.step('User deletion attempt'):
                response = MyRequests.delete(f'{MyRequests.user_registration_uri}/{second_user_id}', 
                                        headers=first_user_headers,
                                        cookies=first_user_cookies)
                 
                Assertions.assert_code_status(response, 400)

