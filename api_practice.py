import os
import re

import pytest
import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


# ---------- Протестировать эндпоинт /api/login ----------
@pytest.fixture
def api_client():
    try:
        api_key = os.environ["X_API_KEY"]  # бросит KeyError, если нет
    except KeyError as e:
        pytest.skip("X_API_KEY not set in env")  # тест отметится SKIPPED
    return {
        "base_url": "https://reqres.in",
        "headers": {"x-api-key": api_key},
    }


@pytest.fixture
def credentials():
    return {
        "email": os.getenv("TEST_EMAIL"),
        "password": os.getenv("TEST_PASSWORD"),
    }


@pytest.mark.parametrize(
    "expected_token_length, token_pattern", [(17, r"^[A-Za-z0-9]{17}$")]
)
def test_login(api_client, credentials, expected_token_length, token_pattern):
    response = requests.post(
        url=f'{api_client["base_url"]}/api/login',
        json=credentials,  # Используем параметр credentials из фикстуры
        headers=api_client["headers"],
    )

    assert response.status_code == 200

    response_data = response.json()
    token = response_data["token"]

    assert token is not None, "Токен отсутствует в ответе"
    assert (
        len(token) == expected_token_length
    ), f"Длина токена {len(token)} вместо ожидаемых {expected_token_length}"
    assert re.fullmatch(
        token_pattern, token
    ), f"Токен не соответствует паттерну {token_pattern}"


# ------------ Протестируй эндпоинт /api/users?page=2 ------------------------
# ------------ на предмет того, что массив data содержит 6 объектов ----------
def test_user_default_count_per_page():
    response = requests.get(
        url=f"https://reqres.in/api/users",
        params={"page": 2},
        headers={"x-api-key": os.getenv("X_API_KEY")},
    )

    assert response.status_code == 200, (  # без .json() до проверки статуса
        f"Ожидался статус 200, получен {response.status_code}. "
        f"Ответ сервера: {response.text}"
    )

    users_count = len(response.json()["data"])
    assert users_count == 6, f"Ожидалось 6 пользователей, получено {users_count}"


# ------------ Протестировать https://reqres.in/api/unknown ------------------
# ------------ В тестовом методе собрать данные в коллекцию. -----------------
# ------------ Проверить, что параметр year каждого объекта >= 2000 ----------
class ColorSample(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class Colors(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[ColorSample]


@pytest.fixture
def api_session():
    session = requests.Session()
    session.headers.update(
        {"x-api-key": os.getenv("X_API_KEY"), "Content-Type": "application/json"}
    )
    yield session
    session.close()


@pytest.fixture
def get_all_colors(api_session) -> Colors:
    all_colors = list()
    base_url = "https://reqres.in/api/unknown"

    response = api_session.get(url=base_url, params={"page": 1}).json()
    total_pages = response["total_pages"]

    all_colors.extend(response["data"])

    for page in range(2, total_pages + 1):
        response = api_session.get(url=base_url, params={"page": page})
        assert (
            response.status_code == 200
        ), f"Page {page} failed with {response.status_code}"
        response = response.json()
        all_colors.extend(response["data"])

    return Colors(
        page=response["page"],
        per_page=response["per_page"],
        total=response["total"],
        total_pages=response["total_pages"],
        data=[ColorSample(**item) for item in all_colors],
    )


def test_color_year(get_all_colors):
    total_colors_count = len(get_all_colors.data)

    years_gte_2000 = [color.year for color in get_all_colors.data if color.year >= 2000]

    assert total_colors_count == len(years_gte_2000)


# ------------ Используя эндпоинт /api/unknown -------------------------------
# ------------ убедись, что поле name у всех объектов из data - не пустое ----
def test_color_name_not_none(get_all_colors):
    total_colors_count = len(get_all_colors.data)
    colors_with_name = [
        color for color in get_all_colors.data if color.name is not None
    ]
    assert len(colors_with_name) == total_colors_count
