import requests

from helper import login_courier, delete_courier, register_new_courier_and_return_login_password, BASE_URL


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
            "first_name": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        # ожидаем статус 409
        assert response.status_code == 409

        # Очищаем данные
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')
        if courier_id:
            delete_courier(courier_id)