import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase

register_user_url = 'https://playground.learnqa.ru/api/user/'
login_user_url = f'{register_user_url}login'

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        register_response = requests.post(register_user_url, data=register_data)

        Assertions.assert_code_status(register_response, 200)
        Assertions.assert_json_has_keys(register_response, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(register_response, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        login_response = requests.post(login_user_url, data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')

        # Edit
        new_name = 'Changed Name'

        edit_response = requests.put(f'{register_user_url}{user_id}',
                                      headers={'x-csrf-token': token},
                                      cookies={'auth_sid': auth_sid},
                                      data={'firstName': new_name})
        
        Assertions.assert_code_status(edit_response, 200)

        # Get user
        get_user_response = requests.get(f'{register_user_url}{user_id}',
                                         headers={'x-csrf-token': token},
                                         cookies={'auth_sid': auth_sid})
        
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', new_name, 
                                             'Wrong name of the user after edit')

