import pytest
import requests
import random
import string
from data import BASE_URL, DEFAULT_PASSWORD, DEFAULT_NAME

@pytest.fixture
def user_data():
    """Создание уникальных данных пользователя"""
    email = f"autotest_{''.join(random.choices(string.ascii_lowercase, k=6))}@yandex.ru"
    return {"email": email, "password": DEFAULT_PASSWORD, "name": DEFAULT_NAME}

@pytest.fixture
def register_user(user_data):
    """Регистрация пользователя и возврат токена"""
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    data = response.json()
    data["token"] = data.get("accessToken", "").split(" ")[1] if "accessToken" in data else None
    return data
