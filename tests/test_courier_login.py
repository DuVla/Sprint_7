import requests
import allure
from helper import (
    login_courier,
    delete_courier,
    generate_random_string
)
from config import BASE_URL


class TestCourierLogin:
    """Тесты для логина курьера"""

    @allure.step("Тест: курьер может авторизоваться")
    def test_courier_can_login(self):
        """Проверка курьер может авторизоваться"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firsName": first_name
        }

        requests.post(f'{BASE_URL}/courier', json=payload)

        login_response = login_courier(login, password)

        assert login_response.status_code == 200
        assert 'id' in login_response.json()
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)

    @allure.step("Тест: неправильный логин ошибка")
    def test_incorrect_login_returns_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать логин"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        # Создаём курьера
        requests.post(f'{BASE_URL}/login', json=payload)
        # Пытаемся логиниться с неправильным логином
        response = login_courier("wrong_login_xyz", password)
        assert response.status_code == 404
        assert 'message' in response.json()
        # Очищаем
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)

    @allure.step("Тест: неправильный пароль ошибка")
    def test_incorrect_password_returns_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать пароль"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        # пытаемся залогиниться с неправильным паролем
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        # Создаём курьера
        requests.post(f'{BASE_URL}/login', json=payload)
        # Пытаемся логиниться с неправильным логином
        response = login_courier(login, "wrong_login_xyz")
        assert response.status_code == 404
        assert 'message' in response.json()

    @allure.step("Тест: без пароля ошибка")
    def test_login_without_password(self):
        """Проверка: без пароля возвращается ошибка"""
        payload = {
            "login": "somelogin"
        }
        response = requests.post(f'{BASE_URL}/courier/login', json=payload)
        assert response.status_code == 504

    @allure.step("Тест: без логина ошибка")
    def test_login_without_login_field(self):
        """Проверка: без логина возвращается ошибка"""
        payload = {
            "password": "somepassword"
        }
        response = requests.post(f'{BASE_URL}/login', json=payload)
        assert response.status_code == 404

    @allure.step("Тест: несуществующий пользователь ошибка")
    def test_nonexistent_user_login_returns_error(self):
        """Проверка: если авторизоваться под несуществующим пользователем, возвращается ошибка"""
        payload = {
            "login": "nonexistent_user12345",
            "password": 'nonexistent_user12345'
        }
        response = requests.post(f'{BASE_URL}/courier/login', json=payload)
        assert response.status_code == 404
        assert 'message' in response.json()

    @allure.step("Тест: успешный логин возвращает ID")
    def test_successful_login_returns_id(self):
        """Проверка: успешный запрос возвращает id"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        # Создаём курьера
        requests.post(f'{BASE_URL}/courier', json=payload)

        # Логинимся
        response = login_courier(login, password)

        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert isinstance(response_data['id'], int)
        assert response_data['id'] > 0

        # Очищаем
        courier_id = response_data['id']
        delete_courier(courier_id)
