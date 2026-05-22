import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import csv

print("QR attendance started")

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    for qr in decode(frame):
        name = qr.data.decode('utf-8')
        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%H:%M:%S")

        with open("attendance.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time, "QR"])

        print(f"Attendance marked for {name}")
        cam.release()
        cv2.destroyAllWindows()
        exit()

    cv2.imshow("QR Attendance", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
