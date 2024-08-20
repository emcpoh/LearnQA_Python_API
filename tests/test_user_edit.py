import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    user_registration_url: str = 'https://playground.learnqa.ru/api/user/'
    user_login_url: str = user_registration_url + 'login'
    user_edit_url: str


    def test_edit_just_created_user(self):
        # Registration
        register_data = self.prepare_registration_data()
        registration_response = requests.post(self.user_registration_url, data=register_data)

        Assertions.assert_code_status(registration_response, 200)
        Assertions.assert_json_has_keys(registration_response, 'id')

        email = register_data['email']
        password = register_data['password']
        first_name = register_data['firstName']
        user_id = self.get_json_value(registration_response, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        login_response = requests.post(self.user_login_url, data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')

        # Edit
        new_name = 'Changed name'
        user_edit_url = f'{self.user_registration_url}{user_id}'
        edit_response = requests.put(user_edit_url,
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid},
                                     data={'firstName': new_name})
        
        Assertions.assert_code_status(edit_response, 200)
        
        # GET
        user_get_url = user_edit_url
        get_user_response = requests.get(user_get_url,
                                         headers={'x-csrf-token': token},
                                         cookies={'auth_sid': auth_sid})
        
        Assertions.assert_json_value_by_name(get_user_response, 'firstName', new_name, 'Wrong name of the user after edit.')
        