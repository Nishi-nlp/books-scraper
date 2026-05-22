from scraper import scrape_books
from exporter import export_to_csv


def main():
    books = scrape_books()

    export_to_csv(books)

    print("CSV exported successfully")


if __name__ == "__main__":
    main()