import requests
from requests import Response
from lib.logger import Logger
import allure

class MyRequests():
    Response: Response
    base_url: str = 'https://playground.learnqa.ru/api'
    user_registration_uri: str = '/user'
    user_login_uri: str = user_registration_uri + '/login'
    user_edit_uri: str

    @staticmethod
    def get (uri: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f'GET request to URL {MyRequests.base_url}{uri}'):
            return MyRequests._send(uri, data, headers, cookies, 'GET')
    
    @staticmethod
    def post (uri: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f'POST request to URL {MyRequests.base_url}{uri}'):
            return MyRequests._send(uri, data, headers, cookies, 'POST')
    
    @staticmethod
    def put (uri: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f'PUT request to URL {MyRequests.base_url}{uri}'):
            return MyRequests._send(uri, data, headers, cookies, 'PUT')
    
    @staticmethod
    def delete (uri: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f'DELETE request to URL {MyRequests.base_url}{uri}'):
            return MyRequests._send(uri, data, headers, cookies, 'DELETE')


    @staticmethod
    def _send(uri: str, data: dict, headers: dict, cookies: dict, method: str):
        request_url = f'{MyRequests.base_url}{uri}'

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        Logger.add_request(request_url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(request_url, params=data, headers=headers, cookies=cookies)

        elif method == 'POST':
            response = requests.post(request_url, data=data, headers=headers, cookies=cookies)

        elif method == 'PUT':
            response = requests.put(request_url, data=data, headers=headers, cookies=cookies)

        elif method == 'DELETE':
            response = requests.delete(request_url, data=data, headers=headers, cookies=cookies)

        else:
            raise Exception(f'Bad HTTP method {method} was received')
        
        Logger.add_response(response)
        
        return response