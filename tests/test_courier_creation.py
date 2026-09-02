import requests

from helper import (login_courier,
                    delete_courier,
                    register_new_courier_and_return_login_password,
                    BASE_URL,
                    generate_random_string)


class TestCourierCreation:
    """Тесты для создания курьера"""

    def test_courier_can_be_created(self):
        """курьера можно создать ПРОВЕРКА"""
        courier_data = register_new_courier_and_return_login_password()

        #Проверяем что функция создала курьера
        assert courier_data is not None
        assert len(courier_data) == 3

        login, password, first_name = courier_data

        # Очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

    def test_courier_cannot_be_created(self):
        """Проверка: нельзя создать двух одинаковых курьеров"""
        # Создаём первого курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data

        # Создаём второго курьера с теми же данными
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        # ожидаем статус 409
        assert response.status_code == 409

        # Очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

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


    def test_duplicate_login_returns_error(self):
        """Проверка: если создать пользователя с логином, который уже есть, возвращается ошибка"""
        # Создаём первого курьера
        courier_data = register_new_courier_and_return_login_password()
        login, password, first_name = courier_data

        # Пытаемся создать второго с ТЕШМ ЖЕ логином но РАЗНЫМИ паролем и именем
        payload = {
            "login": login,  # одинаковый логин
            "password": generate_random_string(10),  # разный пароль
            "firstName": generate_random_string(10)  # разное имя
        }
        response = requests.post(f'{BASE_URL}/courier', json=payload)

        assert response.status_code == 409
        assert 'message' in response.json()

        # очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)

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

        # Очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)