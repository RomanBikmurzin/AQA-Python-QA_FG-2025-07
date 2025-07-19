import re
import time

from playwright.sync_api import Page, expect

LOGIN_URL = "https://github.com/login"
ERROR_LOCATOR = "div.flash-error"  # не юзается теперь
AVATAR_LOCATOR = 'summary[aria-label="View profile and more"]'  # не юзается теперь | измени под то как тебе нужно


class LoginPage:
    def __init__(self, page: Page):  # __init__
        self.page = page

    def username_input(self):
        return self.page.locator("#login_field")

    #
    def password_input(self):
        return self.page.locator("#password")

    # def username_input(self):
    #    return self.page.get_by_label("Username or email address")

    # def password_input(self):
    #    return self.page.get_by_label("Password")  #просто тестил, можно и их использовать

    def login_button(self):
        # return self.page.locator('input[name="commit"]')
        return self.page.locator('input[name="commit"][type="submit"]')  # new

    def navigate(self):
        self.page.goto(LOGIN_URL)  # ???

    def login(self, username: str, password: str):
        expect(self.username_input()).to_be_visible()
        expect(self.password_input()).to_be_visible()

        if username is not None:
            self.username_input().fill(username)
            expect(self.password_input()).to_be_visible()  # не уверен что это нужно

        if password is not None:
            self.password_input().fill(password)

        with self.page.expect_navigation():
            self.login_button().click()

    def error_text(self) -> str:
        return self.page.locator("div.flash-full.flash-error").text_content().strip()

    def avatar_visible(self) -> bool:
        # Было
        # return self.page.locator(AVATAR_LOCATOR).is_visible()
        return self.page.locator(
            'img.avatar.circle[width="32"][height="32"][data-view-component="true"]'
        ).is_visible()
        print(self.page.locator("img.avatar circle").is_visible())
        print(self.page.locator("img.avatar circle"))

        return self.page.locator("img.avatar circle").is_visible()

    def bar_visible(self) -> bool:
        return self.page.locator(
            '[aria-label="Open global navigation menu"]'
        ).is_visible()
        return self.page.locator("user-menu").is_visible()
