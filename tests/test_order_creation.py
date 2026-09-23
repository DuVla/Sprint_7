import requests
import pytest
import allure
from config import BASE_URL
from helper import (
    generate_random_string
)

class TestOrderCreation:
    """Тесты для создания заказа"""

    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    @allure.step("Тест создание заказа с разными цветами")
    def test_create_order_with_colors(self, colors):
        """Проверка: можно указать BLACK, GREY, оба цвета или без цветов"""
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": generate_random_string(10),
            "metroStation": 1,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2026-09-10",
            "comment": "test comment",
            "color": colors
        }

        response = requests.post(f'{BASE_URL}/orders', json=payload)

        assert response.status_code == 201
        assert 'track' in response.json()