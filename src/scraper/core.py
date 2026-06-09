import requests
from bs4 import BeautifulSoup

class PriceScraper:
    def __init__(self, headers=None):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def get_price(self, url: str, price_selector: str) -> float | None:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Rzuca błędem, jeśli strona nie odpowie 200 

            soup = BeautifulSoup(response.text, 'html.parser')
            
            price_element = soup.select_one(price_selector)

            if price_element:
                return self._clean_price(price_element.text)
            
            print(f"Nie znaleziono ceny na stronie (niepoprawny selektor?): {url}")
            return None

        except requests.RequestException as e:
            print(f"Błąd sieci podczas pobierania strony {url}: {e}")
            return None

    def _clean_price(self, raw_price: str) -> float:
        clean_str = raw_price.replace("zł", "").replace("PLN", "").replace(" ", "").replace("\xa0", "").replace(",", ".").strip()
        try:
            return float(clean_str)
        except ValueError:
            print(f"Nie udało się przekonwertować ceny: '{raw_price}'")
            return 0.0