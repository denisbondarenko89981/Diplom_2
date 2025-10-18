import requests
import allure
from urls import BASE_URL


@allure.feature("Создание заказов")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, register_user):
        token = register_user["token"]

        with allure.step("Получаем список ингредиентов"):
            ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:2]
            ingredient_ids = [i["_id"] for i in ingredients]

        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": f"Bearer {token}"},
                json={"ingredients": ingredient_ids}
            )

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Получаем ингредиенты"):
            ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:2]
            ingredient_ids = [i["_id"] for i in ingredients]

        with allure.step("Отправляем запрос без авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ingredient_ids})

        with allure.step("Проверяем ответ"):
            assert response.status_code in [200]
            assert "success" in response.json()

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        with allure.step("Отправляем запрос без ингредиентов"):
            response = requests.post(f"{BASE_URL}/orders", json={"ingredients": []})

        with allure.step("Проверяем сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        with allure.step("Отправляем запрос с неверным ID ингредиента"):
            response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ["invalid_id"]})

        with allure.step("Проверяем ответ об ошибке"):
            assert response.status_code == 500

    @allure.title("Создание заказа с одним ингредиентом")
    def test_create_order_with_single_ingredient(self, register_user):
        token = register_user["token"]

        with allure.step("Получаем один ингредиент"):
            ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:1]
            ingredient_ids = [i["_id"] for i in ingredients]

        with allure.step("Создаём заказ с одним ингредиентом"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": f"Bearer {token}"},
                json={"ingredients": ingredient_ids}
            )

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            assert response.json()["success"] is True
