# src/monitor.py

from src.scraper.core import PriceScraper
from src.scraper.config import SHOPS_SELECTORS
from src.database.db import DatabaseManager

class PriceMonitor:
    def __init__(self):
        self.scraper = PriceScraper()
        self.db = DatabaseManager()

    def update_all_prices(self):
        print("Rozpoczynam sprawdzanie cen dla wszystkich produktów...")
        products = self.db.get_all_products()

        if not products:
            print("Brak produktów w bazie danych do monitorowania.")
            return

        for product in products:
            product_id, name, url, shop_name = product
            
            print(f"\nSprawdzam: {name} ({shop_name})")
            
            selector = SHOPS_SELECTORS.get(shop_name)
            if not selector:
                print(f"BŁĄD: Brak selektora dla sklepu {shop_name} w konfiguracji.")
                continue

            current_price = self.scraper.get_price(url, selector)

            if current_price:
                self.db.add_price_log(product_id, current_price)
                print(f"-> SUKCES: Nowa cena {current_price} PLN zapisana w bazie.")
            else:
                print("-> PORAŻKA: Nie udało się pobrać i zapisać ceny.")
                
        print("\nAktualizacja cen zakończona!")