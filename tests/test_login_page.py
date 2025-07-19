import os
import time

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.login_page import LoginPage

load_dotenv()

VALID_USER = os.getenv("GH_LOGIN")
VALID_PWD = os.getenv("GH_PASSWORD")


@pytest.mark.parametrize(
    "user, pwd, expect_success",
    [
        # ("invalid_user", "invalid_pwd", False),
        ("randj", "2312invalid_pwd", False),
        (VALID_USER, VALID_PWD, True),
    ],
)
def test_login(page: Page, user, pwd, expect_success):
    login = LoginPage(page)
    login.navigate()
    login.login(user, pwd)

    if expect_success:
        assert login.avatar_visible(), "Аватар не отображается"
        assert login.bar_visible(), "Меню пользователя не отображается"

    else:
        assert login.error_text().startswith(
            "Incorrect username or password"
        ), f"Не получили сообщение об ошибке, а увидели: {login.error_text()}"
