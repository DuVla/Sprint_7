import requests
import allure
from helper import (login_courier,
                    delete_courier,
                    generate_random_string)
from config import BASE_URL


class TestCourierCreation:
    """Тесты для создания курьера"""

    @allure.step("Тест: курьера можно создать")
    def test_courier_can_be_created(self):
        """курьера можно создать ПРОВЕРКА"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Очищаем
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)

    @allure.step("Тест: нельзя создать дубликат")
    def test_courier_cannot_be_created(self):
        """Проверка: нельзя создать двух одинаковых курьеров"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # Создаём первого
        requests.post(f'{BASE_URL}/courier', json=payload)

        # Пытаемся создать второго с теми же данными
        response = requests.post(f'{BASE_URL}/courier', json=payload)

        assert response.status_code == 409
        assert 'message' in response.json()

        # Очищаем
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)

    @allure.step("Тест: без пароля ошибка")
    def test_courier_creation_without_password(self):
        """Проверка: без пароля возвращается ошибка"""
        login = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "login": login,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        # Должен вернуть 400
        assert response.status_code == 400
        assert 'message' in response.json()

    @allure.step("Тест: без логина ошибка")
    def test_courier_creation_without_login(self):
        """Проверка: без логина возвращается ошибка"""
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        # Должен вернуть 400
        assert response.status_code == 400
        assert 'message' in response.json()

    @allure.step("Тест: дубликат логина ошибка")
    def test_duplicate_login_returns_error(self):
        """Проверка: логин должен быть уникален"""
        login = generate_random_string(10)
        password1 = generate_random_string(10)
        password2 = generate_random_string(10)

        payload1 = {
            "login": login,
            "password": password1,
            "firstName": generate_random_string(10)
        }

        # Создаём первого
        requests.post(f'{BASE_URL}/courier', json=payload1)

        # Пытаемся создать второго с тем же логином, но другим паролем
        payload2 = {
            "login": login,
            "password": password2,
            "firstName": generate_random_string(10)
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload2)

        assert response.status_code == 409
        assert 'message' in response.json()

        # Очищаем
        login_response = login_courier(login, password1)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)

    @allure.step("Тест: firstName опциональное")
    def test_courier_creation_without_first_name(self):
        """Проверка: firstName опциональное поле"""
        login = generate_random_string(10)
        password = generate_random_string(10)

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        # firstName опциональное - курьер создаётся и без него
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Очищаем
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        delete_courier(courier_id)