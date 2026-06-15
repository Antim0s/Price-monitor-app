from src.gui.app import PriceTrackerApp
from src.database.db import DatabaseManager

def ensure_dummy_data():
    db = DatabaseManager()
    if not db.get_all_products():
        db.add_product(
            name="Książka - horyzont", 
            url="https://www.taniaksiazka.pl/przesunac-horyzont-20-lat-pozniej-p-2473164.html", 
            shop_name="taniaksiazka"
        )
        db.add_product(
            name="Macbook",
            url="https://www.komputronik.pl/product/1014231/apple-macbook-air-m5-10-8-13-6-16gb-512gb-mac-os-srebrny-us.html",
            shop_name="komputronik"
        )

if __name__ == "__main__":
    ensure_dummy_data()
    
    app = PriceTrackerApp()
    app.mainloop()