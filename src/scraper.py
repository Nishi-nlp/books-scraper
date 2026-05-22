from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

URL = "https://books.toscrape.com/"

def scrape_books():
    driver = webdriver.Chrome(
        service=Service("C:\chromedriver-win64\chromedriver.exe")
    )

    driver.get(URL)

    books = []

    while True:
        print("Scraping page...")
        book_elements = driver.find_elements(By.CLASS_NAME, "product_pod")

        for book in book_elements:
                title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")

                price = book.find_element(By.CLASS_NAME, "price_color").text

                rating_element = book.find_element(By.CLASS_NAME, "star-rating")
                rating = rating_element.get_attribute("class").split()[-1]

                link = book.find_element(By.TAG_NAME, "a").get_attribute("href")

                books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": link
                })
        next_buttons = driver.find_elements(By.CLASS_NAME, "next")

        if len(next_buttons) == 0:
            break

        try:
            next_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".next a"))
            )

            next_link.click()
        except TimeoutException:
            print("No next page")
            break

    driver.quit()

    return books