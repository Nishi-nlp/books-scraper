import pytest

from scraper import scrape_books


@pytest.fixture(scope="module")
def books():
    return scrape_books(headless=True, limit=3)


def test_scrape_books_return_list(books):
    assert isinstance(books, list)


def test_scrape_books_not_empty(books):
    assert len(books) > 0


def test_book_has_required_keys(books):
    first_book = books[0]

    required_keys = [
        "title",
        "price",
        "stock",
        "rating",
        "category",
        "url",
    ]

    for key in required_keys:
        assert key in first_book