from datetime import datetime
from requests import Response
import json.decoder
import hashlib
import random
import allure
from lib.my_requests import MyRequests

class BaseCase:
    def prepare_registration_data(self, email=None, username=None, password=None, firstName=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f'{base_part}{random_part}@{domain}'

        if username is None:
            random_value = str(random.random()).encode('utf-8')
            username = hashlib.md5(random_value).hexdigest()

        if password is None:
            random_value = str(random.random()).encode('utf-8')
            password = hashlib.md5(random_value).hexdigest()
        
        if firstName is None:
            random_value = str(random.random()).encode('utf-8')
            firstName = hashlib.md5(random_value).hexdigest()

        return {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': 'learnqa',
            'email': email
        }

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name}'
        cookie = response.cookies.get(cookie_name)
        return cookie

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f'Cann\'notn\' find header with name {header_name}'
        header = response.headers.get(header_name)
        return header

    def get_json_value(self, response: Response, name=None):
        if name == None:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                assert False, f'Response is not in JSON Format. Response text is "{response.text}"'
        else:
            try:
                response_as_dict = response.json()
            except json.decoder.JSONDecodeError:
                assert False, f'Response is not in JSON Format. Response text is "{response.text}"'

            assert name in response_as_dict, f'Response JSON doesnn\'t have key "{name}"'

            return response_as_dict[name]
        
    def invalid_email_generation():
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        invalid_email = f'{base_part}{random_part}{domain}'

        return invalid_email
    
    def register_user(self):
        try:
            with allure.step('Register new user'):
                register_data = self.prepare_registration_data()

                registration_response = MyRequests.post(MyRequests.user_registration_uri, data=register_data)
                email = register_data['email']
                password = register_data['password']
                user_id = self.get_json_value(registration_response, 'id')
        except Exception:
            assert False, 'Some troubles in new user registration'
        
        return email, password, user_id
    
    def login_as_user(self, email, password):
        try:
            login_data = {
                'email': email,
                'password': password
            }

            login_response = MyRequests.post(f'{MyRequests.user_login_uri}', data=login_data)

            auth_sid = self.get_cookie(login_response, 'auth_sid')
            token = self.get_header(login_response, 'x-csrf-token')

            headers = {'x-csrf-token': token}
            cookies = {'auth_sid': auth_sid}
        except Exception:
            assert False, 'Some troubles in user login process'

        return headers, cookies
    
    