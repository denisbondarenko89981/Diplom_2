import requests
import allure
from conftest import BASE_URL
from data import MISSING_FIELD_USER

@allure.feature("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data):
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self, user_data):
        requests.post(f"{BASE_URL}/auth/register", json=user_data)
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Регистрация без обязательного поля")
    def test_create_user_without_required_field(self):
        response = requests.post(f"{BASE_URL}/auth/register", json=MISSING_FIELD_USER)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
