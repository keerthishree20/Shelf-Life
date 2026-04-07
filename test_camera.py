import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

try:
    for _ in range(50):  # scan 50 frames
        ret, frame = cap.read()
        if not ret:
            continue

        barcodes = decode(frame)
        for barcode in barcodes:
            print("Scanned:", barcode.data.decode("utf-8"))
            cap.release()
            exit()

finally:
    cap.release()

print("Camera test done")
