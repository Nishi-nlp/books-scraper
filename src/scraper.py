import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service

from config import (
    BASE_URL,
    CHROMEDRIVER_PATH,
    HEADLESS,
    RETRIES,
    LOG_PATH,
)

from pages.home_page import HomePage
from pages.book_page import BookPage


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_driver(headless=HEADLESS):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1280,900")

    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


def collect_product_urls(driver):
    home_page = HomePage(driver)
    home_page.open(BASE_URL)

    urls = []

    while True:
        books = home_page.get_book_elements()

        for book in books:
            url = book.find_element("css selector", "h3 a").get_attribute("href")
            urls.append(url)

        logging.info(f"Collected URLs: {len(urls)}")

        next_url = home_page.get_next_page_url()

        if not next_url:
            break

        home_page.open(next_url)

    return urls


def scrape_detail(driver, url, retries=RETRIES):
    book_page = BookPage(driver)

    for attempt in range(1, retries + 1):
        try:
            book_page.open(url)

            return {
                "title": book_page.get_title(),
                "price": book_page.get_price(),
                "stock": book_page.get_stock(),
                "rating": book_page.get_rating(),
                "category": book_page.get_category(),
                "url": url,
            }

        except (TimeoutException, WebDriverException) as e:
            logging.warning(f"Retry {attempt}/{retries}: {url} - {e}")
            sleep(1)

    logging.error(f"Failed to scrape: {url}")

    return {
        "title": None,
        "price": None,
        "stock": None,
        "rating": None,
        "category": None,
        "url": url,
    }


def scrape_books(headless=HEADLESS, limit=None):
    driver = create_driver(headless=headless)

    try:
        product_urls = collect_product_urls(driver)
        logging.info(f"Total product URLs: {len(product_urls)}")

        books = []

        for index, url in enumerate(product_urls, start=1):
            if limit and index > limit:
                break

            logging.info(f"Scraping {index}/{len(product_urls)}: {url}")
            books.append(scrape_detail(driver, url))

        return books

    finally:
        driver.quit()