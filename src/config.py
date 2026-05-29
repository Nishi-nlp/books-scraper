from pathlib import Path


BASE_URL = "https://books.toscrape.com/"

HEADLESS = True
TIMEOUT = 10
RETRIES = 3

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

CSV_PATH = DATA_DIR / "books.csv"
EXCEL_PATH = DATA_DIR / "books.xlsx"
LOG_PATH = LOG_DIR / "scraper.log"