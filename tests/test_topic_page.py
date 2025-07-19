import pytest
from playwright.sync_api import Page

from pages.topic_page import TopicPage


@pytest.mark.parametrize(
    "expected_items, expect_success",
    [
        (["AI", "DevOps", "Security", "Software Development", "View all"], True),
        (["AI", "", "Security", "Software Development", "View all"], False),
    ],
)
def test_contact(page: Page, expected_items, expect_success):
    topic = TopicPage(page)
    topic.navigate()
    topic.button_resources().click()
    actual_items = topic.get_items_from_resources()
    if expect_success:
        assert (
            actual_items == expected_items
        ), f"Ожидалось {expected_items}, получено {actual_items}"

    else:
        assert (
            actual_items != expected_items
        ), f"Ожидалось {expected_items}, получено {actual_items}"
