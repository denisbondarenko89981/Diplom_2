import requests
import allure
from conftest import BASE_URL

@allure.feature("Создание заказов")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, register_user):
        token = register_user["token"]
        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:2]
        ingredient_ids = [i["_id"] for i in ingredients]

        response = requests.post(
            f"{BASE_URL}/orders",
            headers={"Authorization": f"Bearer {token}"},
            json={"ingredients": ingredient_ids}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:2]
        ingredient_ids = [i["_id"] for i in ingredients]

        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ingredient_ids})
        assert response.status_code in [200]
        assert "success" in response.json()

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": []})
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ["invalid_id"]})
        assert response.status_code == 500

    @allure.title("Создание заказа с одним ингредиентом")
    def test_create_order_with_single_ingredient(self, register_user):
        token = register_user["token"]
        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"][:1]
        ingredient_ids = [i["_id"] for i in ingredients]

        response = requests.post(
            f"{BASE_URL}/orders",
            headers={"Authorization": f"Bearer {token}"},
            json={"ingredients": ingredient_ids}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
