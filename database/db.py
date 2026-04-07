import sqlite3

DB_PATH = "database/products.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        barcode TEXT PRIMARY KEY,
        name TEXT,
        expiry TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_product(barcode):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, expiry FROM products WHERE barcode=?", (barcode,))
    result = cursor.fetchone()

    conn.close()
    return result
