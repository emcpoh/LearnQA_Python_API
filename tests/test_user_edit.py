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

    @allure.description('This test tries to edit user w/o authorization')
    def test_user_edit_without_auth(self):
        data = self.prepare_registration_data()
        response = MyRequests.put(f'{MyRequests.user_registration_uri}/2',  # хардкожу user_id = 2
                                  data=data)
        
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, '{"error":"Auth token not supplied"}')


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


    # вспомогательная функция для логина в качестве существующего пользователя
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
    
    @allure.description('This test tries to edit user being auth by different user')
    def test_user_edit_auth_diff_user(self):
        data_to_update = self.prepare_registration_data()

        with allure.step('First user registration'):
            first_user_email, first_user_password, first_user_id = self.register_user()


        with allure.step('Second user registration and login'):
            second_user_email, second_user_password, second_user_id = self.register_user()
            second_user_headers, second_user_cookies = self.login_as_user(second_user_email, second_user_password)


        with allure.step(f'Try to edit user with id = {first_user_id} being logged by user with id = {second_user_id}'):
            response = MyRequests.put(f'{MyRequests.user_registration_uri}/{first_user_id}',
                                      cookies=second_user_cookies,
                                      headers=second_user_headers,
                                      data=data_to_update)

        Assertions.assert_code_status(response, 400)
    



    allure.description('This test tries to edit authorized user email to invalid email (w/o @)')
    def test_user_edit_email_to_invalid_one(self):
        email, password, user_id = self.register_user()
        headers, cookies = self.login_as_user(email, password)

        invalid_email = BaseCase.invalid_email_generation()
        data_to_update = self.prepare_registration_data(email=invalid_email)

        response = MyRequests.put(f'{MyRequests.user_registration_uri}/{user_id}',
                                      cookies=cookies,
                                      headers=headers,
                                      data=data_to_update)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, 'error', 'Invalid email format', f'Unexpected response content {response.content}')

    allure.description('This test tries to edit authorized user firstName to a short one')
    def test_user_edit_first_name_to_short_one(self):
        email, password, user_id = self.register_user()
        headers, cookies = self.login_as_user(email, password)

        short_name = 'A'
        data_to_update = self.prepare_registration_data(firstName=short_name)

        response = MyRequests.put(f'{MyRequests.user_registration_uri}/{user_id}',
                                      cookies=cookies,
                                      headers=headers,
                                      data=data_to_update)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(response, 'error', 'The value for field `firstName` is too short', f'Unexpected response content {response.content}')

    


    