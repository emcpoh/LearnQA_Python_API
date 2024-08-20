from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not is JSON format. Response text is {response.text}'
        assert name in response_as_dict, f'Response JSON doesn\'t have key {name}'
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_keys(response: Response, *keys):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'

        for key in keys:
            assert key in response_as_dict, f'Response JSON doesn\'t have key {key}'

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        actual_status_code = response.status_code
        assert actual_status_code == expected_status_code, f'Unexpected status code. Expected - {expected_status_code}. Actual - {actual_status_code}'

    @staticmethod
    def assert_json_has_no_keys(response: Response, *keys):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not is JSON format. Response text is {response.text}'

        for key in keys:
            assert key not in response_as_dict, f'Response JSON shouldn\'t have key {key}, but it present in response.'

    @staticmethod
    def assert_content(response: Response, expected_content):
        # пропускаем проверку за ненадобностью
        if expected_content is None:
            return True
        try:
            decoded_content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            raise UnicodeEncodeError

        assert decoded_content == expected_content, f"Unexpected response content {response.content}"
            


