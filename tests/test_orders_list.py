import requests
import allure
from config import BASE_URL

class TestOrderList:
    """Тесты для получения списка заказов"""

    @allure.step("Тест: список заказов возвращается")
    def test_get_orders_list_return_list(self):
        """в тело ответа возвращается список заказов"""
        response = requests.get(f'{BASE_URL}/orders')
        # Проверяем код ответа
        assert response.status_code == 200
        # Проверяем что в ответе есть orders
        assert 'orders' in response.json()
        # Проверяем orders это список
        assert isinstance(response.json()['orders'], list)

    @allure.step("Тест: статус код 200")
    def test_get_orders_list_correct_status_code(self):
        """получение списка заказов возвращает код 200"""
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200

    @allure.step("Тест: ответ в формате JSON")
    def test_get_orders_list_response_is_json(self):
        """проверка json"""
        response = requests.get(f'{BASE_URL}/orders')

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    @allure.step("Тест: массив заказов в ответе")
    def test_get_orders_list_returns_orders_array(self):
        """в ответе находится массив заказов"""
        response = requests.get(f'{BASE_URL}/orders')

        assert response.status_code == 200
        data = response.json()

        assert 'orders' in data
        orders = data['orders']
        assert isinstance(orders, list)

    @allure.step("Тест: список может быть пустым или заполненным")
    def test_get_orders_list_empty_or_populated(self):
        """Проверка: список заказов может быть пустым или заполненным"""
        response = requests.get(f'{BASE_URL}/orders')

        assert response.status_code == 200
        data = response.json()
        orders = data['orders']

        # Список может быть пустым или содержать заказы
        assert isinstance(orders, list)
        # Длина может быть 0 или больше
        assert len(orders) >= 0