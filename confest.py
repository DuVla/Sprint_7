import pytest
from helper import register_new_courier_and_return_login_password, login_courier, delete_courier


@pytest.fixture
def new_courier():
    """
    Fixture: создаёт нового курьера перед тестом и удаляет после.
    Возвращает кортеж (login, password, first_name, courier_id)
    """
    courier_data = register_new_courier_and_return_login_password()

    if courier_data:
        login, password, first_name = courier_data

        # Получаем ID курьера через логин
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')

        yield login, password, first_name, courier_id

        # Удаляем курьера после теста
        if courier_id:
            delete_courier(courier_id)
    else:
        yield None


@pytest.fixture
def courier_for_deletion():
    """
    Fixture: создаёт курьера для тестов удаления.
    Возвращает (login, password, id)
    """
    courier_data = register_new_courier_and_return_login_password()

    if courier_data:
        login, password, first_name = courier_data
        login_response = login_courier(login, password)
        courier_id = login_response.json().get('id')

        yield login, password, courier_id
    else:
        yield None