from database.db import create_table, get_product, connect_db
from modules.scanner import scan_barcode
from modules.expiry_checker import check_expiry
from modules.alerts import show_alert
from modules.billing import add_to_cart, show_cart

def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO products VALUES ('12345', 'Biscuit', '2026-03-25')")
    cursor.execute("INSERT OR REPLACE INTO products VALUES ('67890', 'Milk', '2026-03-22')")
    cursor.execute("INSERT OR REPLACE INTO products VALUES ('11111', 'Chips', '2026-03-20')")

    conn.commit()
    conn.close()

def main():
    create_table()
    insert_sample_data()

    while True:
        barcode = scan_barcode()
        product = get_product(barcode)

        if product:
            name, expiry = product
            status = check_expiry(expiry)

            show_alert(name, status, expiry)

            if status == "SAFE":
                add_to_cart(name)
            elif status == "NEAR EXPIRY":
                choice = input("Add anyway? (y/n): ")
                if choice.lower() == "y":
                    add_to_cart(name)

        else:
            print("❌ Product not found")

        cont = input("Continue? (y/n): ")
        if cont.lower() != "y":
            break

    show_cart()

if __name__ == "__main__":
    main()
