
import pytest
from src.database.db import DatabaseManager

@pytest.fixture
def memory_db(tmp_path):
    db_path = tmp_path / "test_prices.db"
    
    db = DatabaseManager(db_name=str(db_path))
    yield db

def test_add_and_get_product(memory_db):
    memory_db.add_product("Testowa Klawiatura", "http://test.pl", "komputronik")
    
    products = memory_db.get_all_products()
    
    assert len(products) == 1
    assert products[0][1] == "Testowa Klawiatura"
    assert products[0][2] == "http://test.pl"
    assert products[0][3] == "komputronik"

def test_price_history_sorting(memory_db):
    product_id = memory_db.add_product("Myszka", "http://mysz.pl", "empik")
    
    memory_db.add_price_log(product_id, 100.0)
    memory_db.add_price_log(product_id, 85.0)
    
    history = memory_db.get_price_history(product_id)
    
    assert len(history) == 2
    assert history[0][0] == 85.0
    assert history[1][0] == 100.0

def test_delete_product(memory_db):
    product_id = memory_db.add_product("Gra", "http://gra.pl", "empik")
    memory_db.add_price_log(product_id, 200.0)
    
    memory_db.delete_product(product_id)
    
    assert len(memory_db.get_all_products()) == 0
    assert len(memory_db.get_price_history(product_id)) == 0