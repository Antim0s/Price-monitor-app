from src.monitor import PriceMonitor
from src.database.db import DatabaseManager

def setup_dummy_data():
    db = DatabaseManager()
    products = db.get_all_products()
    
    if not products:
        print("Baza jest pusta. Dodaję testowe produkty...")
        db.add_product(
            name="Horyzont", 
            url="https://www.taniaksiazka.pl/przesunac-horyzont-20-lat-pozniej-p-2473164.html", 
            shop_name="taniaksiazka"
        )
        db.add_product(
            name="MacBook",
            url="https://www.komputronik.pl/product/1014231/apple-macbook-air-m5-10-8-13-6-16gb-512gb-mac-os-srebrny-us.html",
            shop_name="komputronik"
        )

if __name__ == "__main__":
    setup_dummy_data()
    
    monitor = PriceMonitor()
    monitor.update_all_prices()