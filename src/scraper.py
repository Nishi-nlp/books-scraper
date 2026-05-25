import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, CHROMEDRIVER_PATH, HEADLESS, TIMEOUT, RETRIES, LOG_PATH

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


def wait_for_books(driver):
    return WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))
    )


def collect_product_urls(driver):
    driver.get(BASE_URL)

    urls = []

    while True:
        wait_for_books(driver)

        books = driver.find_elements(By.CLASS_NAME, "product_pod")

        for book in books:
            url = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
            urls.append(url)

        logging.info(f"Collected URLs: {len(urls)}")

        next_buttons = driver.find_elements(By.CSS_SELECTOR, ".next a")

        if not next_buttons:
            break

        next_url = next_buttons[0].get_attribute("href")
        driver.get(next_url)

    return urls


def scrape_detail(driver, url, retries=RETRIES):
    for attempt in range(1, retries + 1):
        try:
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product_main h1"))
            )

            title = driver.find_element(By.CSS_SELECTOR, ".product_main h1").text
            price = driver.find_element(By.CLASS_NAME, "price_color").text
            stock = driver.find_element(By.CLASS_NAME, "instock").text.strip()

            rating_element = driver.find_element(By.CLASS_NAME, "star-rating")
            rating = rating_element.get_attribute("class").split()[-1]

            category = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb a")[2].text

            return {
                "title": title,
                "price": price,
                "stock": stock,
                "rating": rating,
                "category": category,
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
            book = scrape_detail(driver, url)
            books.append(book)

        return books

    finally:
        driver.quit()