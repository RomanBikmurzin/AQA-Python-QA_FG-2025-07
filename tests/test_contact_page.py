import pytest
from playwright.sync_api import Page

from pages.contact_page import ContactPage


@pytest.mark.parametrize(
    "first_name, last_name, expect_success",
    [
        ("sasha", "roma", True),
        ("1", "2", True),
        ("", "", False),
    ],
)
def test_contact(page: Page, first_name, last_name, expect_success):
    contact = ContactPage(page)
    contact.navigate()
    contact.button_Solutions().click()
    contact.button_CICD().click()
    contact.button_contact_sales()
    contact.filds_fill(first_name, last_name)

    if expect_success:
        assert contact.fields_is_full(), "Поля заполненны"

    else:
        assert contact.fields_is_clear(), "Поля не заполненны"
