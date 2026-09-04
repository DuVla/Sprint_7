import requests
import random
import string
import allure

from config import BASE_URL


def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


@allure.step("Создать нового курьера")
def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/courier', json=payload)
    return response

@allure.step("Удалить курьера")
def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    response = requests.delete(f'{BASE_URL}/courier/{courier_id}')
    return response

@allure.step("Логин курьера")
def login_courier(login, password):
    """Логинит курьера и возвращает его ID"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/courier/login', json=payload)
    return response