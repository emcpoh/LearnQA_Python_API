import requests


homework_header_url = 'https://playground.learnqa.ru/api/homework_header'

class TestHeader:
    def test_homework_header(self):
        expected_header_name = 'x-secret-homework-header'
        expected_header_value = 'Some secret value'

        response = requests.get(homework_header_url)

        actual_headers = dict(response.headers)
        print(actual_headers)

        assert expected_header_name in actual_headers, f'Expected header is missed in the response headers'

        actual_header_name = expected_header_name
        actual_header_value = actual_headers[actual_header_name]
        
        assert actual_header_value == expected_header_value, f'Actual valie name is not equal to {expected_header_name}'