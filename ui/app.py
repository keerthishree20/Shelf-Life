import tkinter as tk
from database.db import get_product, create_table, connect_db
from modules.expiry_checker import check_expiry
from modules.billing import add_to_cart

# ---------------- SAMPLE DATA ----------------
def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO products VALUES ('12345', 'Biscuit', '2026-03-25')")
    cursor.execute("INSERT OR REPLACE INTO products VALUES ('67890', 'Milk', '2026-03-22')")
    cursor.execute("INSERT OR REPLACE INTO products VALUES ('11111', 'Chips', '2026-03-20')")

    conn.commit()
    conn.close()

# ---------------- BARCODE PROCESS ----------------
def process_barcode(barcode):
    product = get_product(barcode)
    if product:
        name, expiry = product
        status = check_expiry(expiry)

        if status == "EXPIRED":
            result_label.config(text=f"❌ {name} expired!", fg="red")
        elif status == "NEAR EXPIRY":
            result_label.config(text=f"⚠️ {name} near expiry!", fg="orange")
        else:
            result_label.config(text=f"✅ {name} added", fg="green")
            add_to_cart(name)
    else:
        result_label.config(text="❌ Product not found", fg="red")

    entry.delete(0, tk.END)

# ---------------- SCAN FUNCTIONS ----------------
def scan_product_manual():
    barcode = entry.get().strip()
    if barcode:
        process_barcode(barcode)

# ---------------- CART WINDOW ----------------
def show_cart_window():
    from modules.billing import cart

    cart_window = tk.Toplevel(root)
    cart_window.title("🛒 Cart")
    cart_window.geometry("250x200")

    tk.Label(cart_window, text="Cart Items", font=("Arial", 14)).pack(pady=5)

    if not cart:
        tk.Label(cart_window, text="Cart is empty").pack()
    else:
        for item in cart:
            tk.Label(cart_window, text=item).pack()

# ---------------- MAIN UI ----------------
root = tk.Tk()
root.title("ShelfLife Sentinel")
root.geometry("300x300")

# Initialize DB & sample data
create_table()
insert_sample_data()
print("Database initialized")

# UI Elements
tk.Label(root, text="Scan Barcode", font=("Arial", 12)).pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

# Manual scan button
scan_manual_btn = tk.Button(root, text="⌨️ Enter Manually", command=scan_product_manual)
scan_manual_btn.pack(pady=5)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 10))
result_label.pack(pady=10)

# Show Cart button
cart_btn = tk.Button(root, text="Show Cart", command=show_cart_window)
cart_btn.pack(pady=5)

# Run the app
root.mainloop()