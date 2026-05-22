import cv2
import os

name = input("Enter student name: ")
path = f"dataset/{name}"
os.makedirs(path, exist_ok=True)

cam = cv2.VideoCapture(0)
count = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"Images Captured: {count}/10",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("Face Capture", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) == 1:
        face_img = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{path}/{count}.jpg", face_img)
        count += 1
        print(f"Captured image {count}")

    if count == 10 or key == 27:
        break

cam.release()
cv2.destroyAllWindows()

# import cv2
# import os

# name = input("Enter student name: ")
# path = f"dataset/{name}"
# os.makedirs(path, exist_ok=True)

# cam = cv2.VideoCapture(0)
# count = 0

# while True:
#     ret, frame = cam.read()
#     cv2.imshow("Capture Face", frame)

#     if cv2.waitKey(1) & 0xFF == ord('s'):
#         cv2.imwrite(f"{path}/{count}.jpg", frame)
#         count += 1
#         print("Image saved")

#     if count == 10:
#         break

# cam.release()
# cv2.destroyAllWindows()
