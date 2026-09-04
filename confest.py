import pytest
import requests
from helper import login_courier, delete_courier, generate_random_string
from config import BASE_URL

@pytest.fixture
def new_courier():
    """
        Fixture: создаёт нового курьера перед тестом и удаляет после.
        Возвращает (login, password, first_name, courier_id)
        """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    # Создаём курьера
    response = requests.post(f'{BASE_URL}/courier', json=payload)

    # Логинимся и получаем ID
    login_response = login_courier(login, password)
    courier_id = login_response.json().get('id')

    # Отдаём данные тесту
    yield login, password, first_name, courier_id

    # ОЧИЩАЕМ - удаляем курьера ВСЕГДА (без if!)
    delete_courier(courier_id)