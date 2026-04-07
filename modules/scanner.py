import cv2
from pyzbar.pyzbar import decode
from database.db import get_product, create_table, connect_db
from modules.expiry_checker import check_expiry

# Initialize DB
create_table()

# Sample cart
cart = []

# Sample data
conn = connect_db()
cursor = conn.cursor()
cursor.execute("INSERT OR REPLACE INTO products VALUES ('12345', 'Biscuit', '2026-03-25')")
cursor.execute("INSERT OR REPLACE INTO products VALUES ('67890', 'Milk', '2026-03-22')")
cursor.execute("INSERT OR REPLACE INTO products VALUES ('11111', 'Chips', '2026-03-20')")
conn.commit()
conn.close()

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("📷 Camera opened. Press 'q' to finish scanning.\n")

scanned = set()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    barcodes = decode(frame)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        if barcode_data in scanned:
            continue  # skip duplicates
        scanned.add(barcode_data)

        product = get_product(barcode_data)
        if product:
            name, expiry = product
            status = check_expiry(expiry)
            if status == "EXPIRED":
                print(f"❌ {name} expired, not added")
            elif status == "NEAR EXPIRY":
                print(f"⚠️ {name} near expiry, added to cart anyway")
                cart.append(name)
            else:
                print(f"✅ {name} added to cart")
                cart.append(name)
        else:
            print(f"❌ Product {barcode_data} not found")

        # Draw rectangle and text
        for b in barcodes:
            x, y, w, h = b.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, barcode_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Barcode Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Final cart summary
print("\n🛒 Final Cart Items:")
if not cart:
    print("Cart is empty")
else:
    for idx, item in enumerate(cart, start=1):
        print(f"{idx}. {item}")