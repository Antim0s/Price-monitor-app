import sqlite3
from typing import List, Tuple

class DatabaseManager:
    def __init__(self, db_name: str = "prices.db"):
        self.db_name = db_name
        self._create_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    shop_name TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    price REAL NOT NULL,
                    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(product_id) REFERENCES products(id)
                )
            ''')
            conn.commit()

    def add_product(self, name: str, url: str, shop_name: str) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO products (name, url, shop_name) VALUES (?, ?, ?)",
                    (name, url, shop_name)
                )
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                cursor.execute("SELECT id FROM products WHERE url = ?", (url,))
                return cursor.fetchone()[0]

    def add_price_log(self, product_id: int, price: float):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
                (product_id, price)
            )
            conn.commit()

    def get_all_products(self) -> List[Tuple]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, url, shop_name FROM products")
            return cursor.fetchall()