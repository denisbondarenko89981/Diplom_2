import requests
import allure
from urls import BASE_URL
from data import INVALID_EMAIL, INVALID_PASSWORD


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация существующего пользователя")
    def test_login_existing_user(self, user_data):
        with allure.step("Регистрируем пользователя"):
            requests.post(f"{BASE_URL}/auth/register", json=user_data)

        with allure.step("Выполняем авторизацию зарегистрированного пользователя"):
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Авторизация с неверным логином и паролем")
    def test_login_with_invalid_credentials(self):
        with allure.step("Пробуем авторизоваться с неверными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": INVALID_EMAIL,
                "password": INVALID_PASSWORD
            })

        with allure.step("Проверяем сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"
