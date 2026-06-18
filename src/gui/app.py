import customtkinter as ctk
import threading
import webbrowser 
from src.database.db import DatabaseManager
from src.monitor import PriceMonitor
from src.scraper.config import SHOPS_SELECTORS 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import sys

ctk.set_appearance_mode("System")  # System, Dark, lub Light
ctk.set_default_color_theme("blue")

class PriceTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        self.monitor = PriceMonitor()

        self.title("Monitor Cen Produktów")
        self.geometry("900x600")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
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

        self.autopilot_var = ctk.StringVar(value="off")
        self.autopilot_switch = ctk.CTkSwitch(
            self.sidebar_frame, 
            text="🔄 Autopilot (1h)", 
            command=self.toggle_autopilot,
            variable=self.autopilot_var, 
            onvalue="on", 
            offvalue="off",
            button_color="#2ecc71" 
        )
        self.autopilot_switch.grid(row=3, column=0, padx=20, pady=10)

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

            btn_container = ctk.CTkFrame(card, fg_color="transparent")
            btn_container.pack(side="right", padx=10)

            delete_btn = ctk.CTkButton(
                btn_container, 
                text="🗑️ Usuń", 
                width=70, 
                fg_color="#c0392b", 
                hover_color="#e74c3c", 
                command=lambda p=prod_id: self.delete_product_action(p)
            )
            delete_btn.pack(side="right", padx=5)

            # Przycisk historii
            history_btn = ctk.CTkButton(
                btn_container, 
                text="📈 Historia", 
                width=90, 
                fg_color="#34495e", 
                hover_color="#2c3e50",
                command=lambda p=prod_id, n=name: self.open_history_dialog(p, n)
            )
            history_btn.pack(side="right", padx=5)

            latest_data = self.db.get_latest_price(prod_id)

            if latest_data:
                price, date = latest_data
                date_str = date[:16]
                price_text = f"{price} PLN"
                date_text = f"Aktualizacja: {date_str}"
                
                price_container = ctk.CTkFrame(card, fg_color="transparent")
                price_container.pack(side="right", padx=10, pady=5)
                
                ctk.CTkLabel(price_container, text=price_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#2ecc71").pack(anchor="e")
                ctk.CTkLabel(price_container, text=date_text, font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="e")
            else:
                ctk.CTkLabel(card, text="Brak pobranej ceny", font=ctk.CTkFont(size=14, slant="italic"), text_color="gray").pack(side="right", padx=20)


    def update_prices_thread(self):
        self.refresh_btn.configure(state="disabled", text="Pobieranie...")
        
        def run_monitor():
            self.monitor.update_all_prices()
            
            self.after(0, self._finish_update_prices)

        threading.Thread(target=run_monitor, daemon=True).start()

    def _finish_update_prices(self):
        self.refresh_btn.configure(state="normal", text="Sprawdź teraz ceny")
        self.refresh_product_list()
    

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
                "taniaksiazka": "https://www.taniaksiazka.pl",
                "militaria": "https://e-militaria.pl/",
                "vobis": "https://vobis.pl",
                "gandalf": "https://www.gandalf.com.pl"
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



    def open_history_dialog(self, product_id: int, product_name: str):
        history_window = ctk.CTkToplevel(self)
        history_window.title(f"Historia cen: {product_name}")
        history_window.geometry("750x650") 
        
        history_window.transient(self)
        history_window.grab_set()

        title_lbl = ctk.CTkLabel(history_window, text=product_name, font=ctk.CTkFont(size=18, weight="bold"))
        title_lbl.pack(pady=(15, 5), padx=20)

        history_data = self.db.get_price_history(product_id)

        if not history_data:
            ctk.CTkLabel(history_window, text="Brak historii cen dla tego produktu.", font=ctk.CTkFont(size=14)).pack(pady=50)
            return

        
        chronological_data = list(reversed(history_data))
        dates = [row[1][5:16].replace("-", ".") for row in chronological_data] # Ucinamy rok, zostawiamy MM.DD HH:MM
        prices = [row[0] for row in chronological_data]

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
        fig.patch.set_facecolor('#242424')  
        ax.set_facecolor('#242424')         
        
        ax.plot(dates, prices, marker='o', color='#2ecc71', linewidth=2, markersize=6)
        
        ax.tick_params(axis='x', colors='white', rotation=15)
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=history_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=20, fill="x")

        scroll_frame = ctk.CTkScrollableFrame(history_window, width=700, height=200)
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header_frame, text="Data sprawdzenia", font=ctk.CTkFont(weight="bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="Cena", font=ctk.CTkFont(weight="bold")).pack(side="right")

        separator = ctk.CTkFrame(scroll_frame, height=2, fg_color="gray50")
        separator.pack(fill="x", padx=5, pady=5)

        for price, check_date in history_data:
            row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            
            formatted_date = check_date[:16].replace("-", ".")
            ctk.CTkLabel(row, text=formatted_date, font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkLabel(row, text=f"{price} PLN", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2ecc71").pack(side="right")


    def delete_product_action(self, product_id: int):
        self.db.delete_product(product_id)
        self.refresh_product_list()



    def toggle_autopilot(self):
        if self.autopilot_var.get() == "on":
            self.run_autopilot_cycle()

    def run_autopilot_cycle(self):
        if self.autopilot_var.get() == "on":
            self.update_prices_thread()
            self.after(3600000, self.run_autopilot_cycle)


    
    def on_closing(self):
        print("Zamykanie aplikacji...")
        self.autopilot_var.set("off") 
        
        self.quit()     
        self.destroy()  
        sys.exit(0)    