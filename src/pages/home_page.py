from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    def get_book_elements(self):
        return self.driver.find_elements(
            By.CLASS_NAME,
            "product_pod"
        )

    def get_next_page_url(self):
        next_buttons = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".next a"
        )

        if next_buttons:
            return next_buttons[0].get_attribute("href")

        return None