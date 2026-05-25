from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BookPage(BasePage):
    def get_title(self):
        return self.driver.find_element(
            By.CSS_SELECTOR,
            ".product_main h1"
        ).text

    def get_price(self):
        return self.driver.find_element(
            By.CLASS_NAME,
            "price_color"
        ).text

    def get_stock(self):
        return self.driver.find_element(
            By.CLASS_NAME,
            "instock"
        ).text.strip()

    def get_rating(self):
        rating_element = self.driver.find_element(
            By.CLASS_NAME,
            "star-rating"
        )
        return rating_element.get_attribute("class").split()[-1]

    def get_category(self):
        return self.driver.find_elements(
            By.CSS_SELECTOR,
            ".breadcrumb a"
        )[2].text