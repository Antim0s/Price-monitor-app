import cloudscraper
from bs4 import BeautifulSoup

class PriceScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )

    def get_price(self, url: str, price_selector: str) -> float | None:

        try:
            response = self.scraper.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            price_element = soup.select_one(price_selector)

            if price_element:
                if price_element.name == 'meta' and price_element.has_attr('content'):
                    raw_price = price_element['content']
                else:
                    raw_price = price_element.text
                    
                return self._clean_price(raw_price)
            
            print(f"Nie znaleziono ceny na stronie (niepoprawny selektor?): {url}")
            return None

        except Exception as e:
            print(f"Błąd podczas pobierania strony przez cloudscraper {url}: {e}")
            return None

    def _clean_price(self, raw_price: str) -> float:
        clean_str = raw_price.replace("zł", "").replace("PLN", "").replace(" ", "").replace("\xa0", "").replace(",", ".").strip()
        try:
            return float(clean_str)
        except ValueError:
            print(f"Nie udało się przekonwertować ceny: '{raw_price}'")
            return 0.0