from unittest.mock import patch
import pytest
from src.scraper.core import PriceScraper

@pytest.fixture
def scraper():
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


def test_clean_price_regex():
    scraper = PriceScraper()
    dirty_text = "\n                                        249,99\xa0zł\n    "
    clean_price = scraper._clean_price(dirty_text)
    
    assert clean_price == 249.99

def test_get_price_network_error():
    scraper = PriceScraper()
    
    with patch.object(scraper.scraper, 'get', side_effect=Exception("Symulowany brak internetu/odmowa dostępu!")):
        
        price = scraper.get_price("https://sklep.pl/produkt", "span.price")
        
        assert price == 0.0