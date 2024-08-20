from datetime import datetime
from requests import Response
import json.decoder

class BaseCase:
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f'{base_part}{random_part}@{domain}'
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
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