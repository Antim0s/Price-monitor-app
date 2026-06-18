import cloudscraper
from bs4 import BeautifulSoup
import re

class PriceScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )

    def get_price(self, url: str, selector: str) -> float:
        try:
            headers = {
                "ngrok-skip-browser-warning": "true"
            }
            
            response = self.scraper.get(url, timeout=15, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            for sel in selector.split(','):
                element = soup.select_one(sel.strip())
                if element:
                    price_text = element.get('content') if element.name == 'meta' else element.text
                    return self._clean_price(price_text)

            print(f"Nie znaleziono ceny na stronie (niepoprawny selektor?): {url}")
            return 0.0

        except Exception as e:
            print(f"Błąd podczas scrapowania {url}: {e}")
            return 0.0

    def _clean_price(self, price_str: str) -> float:
        if not price_str:
            return 0.0
            
        try:
            text = price_str.replace('\xa0', '').replace(' ', '').replace(',', '.')
            
            clean_text = re.sub(r'[^\d.]', '', text)
            
            return float(clean_text)
        except Exception as e:
            print(f"Błąd podczas czyszczenia ceny '{price_str}': {e}")
            return 0.0