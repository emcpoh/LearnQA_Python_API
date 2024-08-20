import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic('User edit cases')
class TestUserEdit(BaseCase):
    @allure.description('This test edit just created user')
    def test_edit_just_created_user(self):
        with allure.step('User registration'):
            register_data = self.prepare_registration_data()
            registration_response = MyRequests.post(MyRequests.user_registration_uri, data=register_data)

            Assertions.assert_code_status(registration_response, 200)
            Assertions.assert_json_has_keys(registration_response, 'id')

        email = register_data['email']
        password = register_data['password']
        first_name = register_data['firstName']
        user_id = self.get_json_value(registration_response, 'id')

        with allure.step('User login'):
            login_data = {
                'email': email,
                'password': password
            }

            login_response = MyRequests.post(MyRequests.user_login_uri, data=login_data)

            auth_sid = self.get_cookie(login_response, 'auth_sid')
            token = self.get_header(login_response, 'x-csrf-token')

        with allure.step('User edit'):
            new_name = 'Changed name'
            user_edit_uri = f'{MyRequests.user_registration_uri}/{user_id}'
            edit_response = MyRequests.put(user_edit_uri,
                                    headers={'x-csrf-token': token},
                                    cookies={'auth_sid': auth_sid},
                                    data={'firstName': new_name})
            
            Assertions.assert_code_status(edit_response, 200)
        
        with allure.step('User get'):
            user_get_uri = user_edit_uri
            get_user_response = MyRequests.get(user_get_uri,
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid})
            
            Assertions.assert_json_value_by_name(get_user_response, 'firstName', new_name, 'Wrong name of the user after edit.')
        