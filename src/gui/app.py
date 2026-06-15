import customtkinter as ctk
import threading
from src.database.db import DatabaseManager
from src.monitor import PriceMonitor

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

        self.add_btn = ctk.CTkButton(self.sidebar_frame, text="+ Dodaj produkt", fg_color="transparent", border_width=2)
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

    def update_prices_thread(self):
        self.refresh_btn.configure(state="disabled", text="Pobieranie...")
        
        def run_monitor():
            self.monitor.update_all_prices()
            self.refresh_btn.configure(state="normal", text="Sprawdź teraz ceny")
            self.refresh_product_list()

        threading.Thread(target=run_monitor, daemon=True).start()