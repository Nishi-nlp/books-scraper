from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://books.toscrape.com/"

def scrape_books():
    driver = webdriver.Chrome(
        service=Service("C:\chromedriver-win64\chromedriver.exe")
    )

    driver.get(URL)

    books = []

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

    driver.quit()

    return books