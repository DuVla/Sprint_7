from helper import (
    login_courier,
    delete_courier,
    register_new_courier_and_return_login_password,
    BASE_URL,
    generate_random_string
)
import requests

class TestCourierLogin:
    """Тесты для логина курьера"""

    def test_courier_can_login(self):
        """Проверка курьер может авторизоваться"""
        # создаем курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        # логинимся
        response = login_courier(login, password)
        # чекаем код ответа
        assert response.status_code == 200
        # чекаем код id
        assert 'id' in response.json()
        # чистим данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

    def test_incorrect_login_returns_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать логин"""
        # создаем курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        # пытаемся залогиниться с неправильным логином
        payload = {
            "login": "wrond_login12345",
            "password": password
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404
        assert 'message' in response.json()
        # чистим данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

    def test_incorrect_password_returns_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать пароль"""
        # создаем курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data
        # пытаемся залогиниться с неправильным паролем
        payload = {
            "login": login,
            "password": 'wrond_login12345'
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404
        assert 'message' in response.json()
        # чистим данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

    def test_login_without_password(self):
        """Проверка: без пароля возвращается ошибка"""
        payload = {
            "login": "login"
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404

    def test_login_without_login_field(self):
        """Проверка: без логина возвращается ошибка"""
        payload = {
            "password": "password"
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404

    def test_nonexistent_user_login_returns_error(self):
        """Проверка: если авторизоваться под несуществующим пользователем, возвращается ошибка"""
        payload = {
            "login": "nonexistent_user12345",
            "password": 'nonexistent_user12345'
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404
        assert 'message' in response.json()

    def test_successful_login_returns_id(self):
        """Проверка: успешный запрос возвращает id"""
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data

        response = login_courier(login, password)
        # Проверяем код ответа
        assert response.status_code == 200
        # Проверяем что в ответе есть ID
        response_data = response.json()
        assert 'id' in response.json()
        # ID должен быть числом и больше 0
        assert isinstance(response.json()['id'], int)
        assert response_data['id'] > 0
        # очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)