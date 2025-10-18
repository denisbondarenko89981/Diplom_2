import requests
import allure
import pytest
from urls import BASE_URL


@allure.feature("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data):
        with allure.step("Регистрируем нового пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        with allure.step("Проверяем успешную регистрацию"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self, user_data):
        with allure.step("Создаём пользователя"):
            requests.post(f"{BASE_URL}/auth/register", json=user_data)
        with allure.step("Пытаемся создать того же пользователя ещё раз"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        with allure.step("Проверяем сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @pytest.mark.parametrize("missing_field, user_data", [
        ("email", {"password": "123456", "name": "AutoTest"}),
        ("password", {"email": "test1@yandex.ru", "name": "AutoTest"}),
        ("name", {"email": "test2@yandex.ru", "password": "123456"})
    ])
    @allure.title("Регистрация без обязательного поля")
    def test_create_user_without_required_field(self, missing_field, user_data):
        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        with allure.step("Проверяем сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["message"] == "Email, password and name are required fields"
