# tests/test_scraper.py

import pytest
from src.scraper.core import PriceScraper

@pytest.fixture
def scraper():
    """Przygotowuje instancję scrapera przed każdym testem."""
    return PriceScraper()

def test_clean_price_standard(scraper):
    result = scraper._clean_price("4 799,00 zł")
    assert result == 4799.0

def test_clean_price_pln(scraper):
    result = scraper._clean_price("150.50 PLN")
    assert result == 150.5

def test_clean_price_hard_spaces(scraper):
    result = scraper._clean_price(" 1\xa0299 , 99 zł ")
    assert result == 1299.99

def test_clean_price_invalid_string(scraper):
    result = scraper._clean_price("Brak towaru")
    assert result == 0.0