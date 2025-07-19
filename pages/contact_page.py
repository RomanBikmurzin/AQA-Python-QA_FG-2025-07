from playwright.sync_api import Page

GITHUB_URL = "https://github.com/"


class ContactPage:
    def __init__(self, page: Page):
        self.page = page

    def firstname_input(self):
        return self.page.locator('input[name="first_name"]')

    def lastname_input(self):
        return self.page.locator('input[name="last_name"]')

    def navigate(self):
        self.page.goto(GITHUB_URL)

    def button_Solutions(self):
        return self.page.locator('button.HeaderMenu-link:has-text("Solutions")')

    def button_CICD(self):
        return self.page.locator('a.HeaderMenu-dropdown-link:has-text("CI/CD")')

    def button_contact_sales(self):
        # не знаю зачем, но можно перейти по ссылке
        contact_sales_url = self.page.locator(
            'a:has-text("Contact sales"):visible'
        ).first.get_attribute("href")
        # return self.page.locator('a:has-text("Contact sales"):visible').first
        return self.page.goto(contact_sales_url)

    def filds_fill(self, first_name, last_name):
        self.firstname_input().fill(first_name)
        self.lastname_input().fill(last_name)

    def fields_is_full(self):
        return (self.firstname_input().input_value() != "") and (
            self.lastname_input().input_value() != ""
        )

    def fields_is_clear(self):
        return (self.firstname_input().input_value() == "") and (
            self.lastname_input().input_value() == ""
        )
