from plyer import notification  
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
            #current_price = 25.00

            if current_price:
                latest_db_data = self.db.get_latest_price(product_id)
                
                if latest_db_data:
                    old_price, _ = latest_db_data
                    self._check_price_change(name, old_price, current_price)
                else:
                    print("-> To pierwsze sprawdzenie tego produktu. Brak historii do porównania.")

                self.db.add_price_log(product_id, current_price)
                print(f"-> SUKCES: Nowa cena {current_price} PLN zapisana w bazie.")
            else:
                print("-> PORAŻKA: Nie udało się pobrać i zapisać ceny.")
                
        print("\nAktualizacja cen zakończona!")

    def _check_price_change(self, product_name: str, old_price: float, new_price: float):
        if new_price < old_price:
            roznica = round(old_price - new_price, 2)
            title = "📉 Okazja! Cena spadła!"
            message = f"Produkt '{product_name}' staniał o {roznica} PLN!\nStara cena: {old_price} PLN -> Nowa: {new_price} PLN"
            self._send_notification(title, message)
            
        elif new_price > old_price:
            roznica = round(new_price - old_price, 2)
            title = "📈 Podwyżka ceny!"
            message = f"Produkt '{product_name}' podrożał o {roznica} PLN.\nStara cena: {old_price} PLN -> Nowa: {new_price} PLN"
            self._send_notification(title, message)
        else:
            print("-> Cena bez zmian.")

    def _send_notification(self, title: str, message: str):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Price Tracker",
                timeout=7  
            )
            print(f"-> Wysłano powiadomienie: {title}")
        except Exception as e:
            print(f"-> Błąd podczas wysyłania powiadomienia: {e}")