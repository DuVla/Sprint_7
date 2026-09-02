import requests
from helper import (
    generate_random_string,
    BASE_URL
)

class TestOrderCreation:
    """Тесты для создания заказа"""

    def test_create_oder_with_black_color(self):
        """Проверка: можно указать цвет BLACK"""
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(10),
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2026-09-10",
            "comment": "Тестирование черного",
            "color": ["BLACK"]
}
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        #статут чек и трек чек
        assert response.status_code == 201
        assert 'track' in response.json()



    def test_create_order_with_grey_color(self):
        """Проверка: можно указать цвет GRAY"""
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(10),
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2026-09-10",
            "comment": "Тестирование коричневого",
            "color": ["GRAY"]
        }
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        # статут чек и трек чек
        assert response.status_code == 201
        assert 'track' in response.json()

    def test_create_order_with_both_color(self):
        """Проверка: можно указать цвет GRAY and BLACK"""
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(10),
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2026-09-10",
            "comment": "Тестирование коричневого",
            "color": ["BLACK","GRAY"]
        }
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        # статут чек и трек чек
        assert response.status_code == 201
        assert 'track' in response.json()

    def test_create_order_without_color(self):
        """Проверка: можно указать цвет GRAY and BLACK"""
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(10),
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2026-09-10",
            "comment": "Тестирование коричневого",
            "color": []
        }
        response = requests.post(f'{BASE_URL}/orders', json=payload)
        assert response.status_code == 201
        assert 'track' in response.json()