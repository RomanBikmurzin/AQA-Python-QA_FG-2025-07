from playwright.sync_api import Page

GITHUB_URL = "https://github.com/"


class TopicPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(GITHUB_URL)

    def button_resources(self):
        return self.page.locator('button.HeaderMenu-link:has-text("Resources")')

    def get_items_from_resources(self):
        # print(self.page.locator("ul.list-style-none li").all_text_contents())
        # print(self.page.locator("ul.list-style-none li").locator('li:visible a').all_text_contents())
        items = [
            text.strip()
            for text in self.page.locator(
                'ul[aria-labelledby="resources-topics-heading"] li'
            ).all_text_contents()
        ]
        return items
