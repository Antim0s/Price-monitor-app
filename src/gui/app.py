import customtkinter as ctk
import threading
import webbrowser 
from src.database.db import DatabaseManager
from src.monitor import PriceMonitor
from src.scraper.config import SHOPS_SELECTORS  

ctk.set_appearance_mode("System")  # System, Dark, lub Light
ctk.set_default_color_theme("blue")

class PriceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        self.monitor = PriceMonitor()

        self.title("Monitor Cen Produktów")
        self.geometry("900x600")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_frame()
        self.refresh_product_list()

    def _create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Price Tracker", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.refresh_btn = ctk.CTkButton(self.sidebar_frame, text="Sprawdź teraz ceny", command=self.update_prices_thread)
        self.refresh_btn.grid(row=1, column=0, padx=20, pady=10)

        self.add_btn = ctk.CTkButton(self.sidebar_frame, text="+ Dodaj produkt", fg_color="transparent", border_width=2, command=self.open_add_product_dialog)
        self.add_btn.grid(row=2, column=0, padx=20, pady=10)

    def _create_main_frame(self):
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def refresh_product_list(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        products = self.db.get_all_products()
        
        if not products:
            lbl = ctk.CTkLabel(self.main_frame, text="Brak produktów. Dodaj coś do śledzenia!", font=ctk.CTkFont(size=16))
            lbl.pack(pady=50)
            return

        for prod in products:
            prod_id, name, url, shop_name = prod
            
            card = ctk.CTkFrame(self.main_frame, fg_color=("gray85", "gray16"))
            card.pack(fill="x", padx=10, pady=10)
            
            name_lbl = ctk.CTkLabel(card, text=f"{name} ({shop_name})", font=ctk.CTkFont(size=16, weight="bold"))
            name_lbl.pack(side="left", padx=20, pady=15)

            latest_data = self.db.get_latest_price(prod_id)

            if latest_data:
                price, date = latest_data
                date_str = date[:16]
                price_text = f"{price} PLN"
                date_text = f"Aktualizacja: {date_str}"
                
                price_container = ctk.CTkFrame(card, fg_color="transparent")
                price_container.pack(side="right", padx=20, pady=5)
                
                ctk.CTkLabel(price_container, text=price_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#2ecc71").pack(anchor="e")
                ctk.CTkLabel(price_container, text=date_text, font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="e")
            else:
                ctk.CTkLabel(card, text="Brak pobranej ceny", font=ctk.CTkFont(size=14, slant="italic"), text_color="gray").pack(side="right", padx=20)

    def update_prices_thread(self):
        self.refresh_btn.configure(state="disabled", text="Pobieranie...")
        
        def run_monitor():
            self.monitor.update_all_prices()
            self.refresh_btn.configure(state="normal", text="Sprawdź teraz ceny")
            self.refresh_product_list()

        threading.Thread(target=run_monitor, daemon=True).start()
    

    def open_add_product_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Dodaj nowy produkt")
        dialog.geometry("450x450")
        
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Wybierz sklep:", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        
        shop_combo = ctk.CTkComboBox(dialog, values=list(SHOPS_SELECTORS.keys()), width=300)
        shop_combo.pack(pady=5)

        def open_browser():
            shop = shop_combo.get()
            urls = {
                "komputronik": "https://www.komputronik.pl",
                "taniaksiazka": "https://www.taniaksiazka.pl"
            }
            if shop in urls:
                webbrowser.open(urls[shop])

        ctk.CTkButton(dialog, text="🌐 Otwórz wybrany sklep w przeglądarce", fg_color="#34495e", hover_color="#2c3e50", command=open_browser).pack(pady=(5, 15))

        ctk.CTkLabel(dialog, text="Nazwa produktu (własna):", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        name_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="np. Książka Wiedźmin")
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Link do produktu (URL):", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
        url_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="Wklej skopiowany link...")
        url_entry.pack(pady=5)

        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)

        def save_action():
            name = name_entry.get().strip()
            url = url_entry.get().strip()
            shop = shop_combo.get()

            if not name or not url:
                error_label.configure(text="Uzupełnij nazwę i wklej link!")
                return
            
            if "http" not in url:
                error_label.configure(text="Link musi zawierać http/https!")
                return

            self.db.add_product(name, url, shop)
            self.refresh_product_list()
            dialog.destroy() 

        ctk.CTkButton(dialog, text="✔ Zapisz produkt", command=save_action, fg_color="#27ae60", hover_color="#2ecc71").pack(pady=(10, 20))