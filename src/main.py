from config import CSV_PATH, EXCEL_PATH, DATA_DIR, LOG_DIR
from scraper import scrape_books
from exporter import export_to_csv, export_to_excel


def main():
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    
    books = scrape_books()

    export_to_csv(books, CSV_PATH)
    export_to_excel(books, EXCEL_PATH)

    print(f"Done. {len(books)} books exported.")


if __name__ == "__main__":
    main()