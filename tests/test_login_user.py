import requests
import allure
from conftest import BASE_URL
from data import INVALID_EMAIL, INVALID_PASSWORD

@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_existing_user(self, user_data):
        requests.post(f"{BASE_URL}/auth/register", json=user_data)
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Авторизация с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": INVALID_EMAIL,
            "password": INVALID_PASSWORD
        })
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
