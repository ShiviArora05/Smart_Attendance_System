import cv2
import os
import numpy as np
from datetime import datetime
import csv
import time

print("Face attendance (CLASS MODE) started")

dataset_path = "dataset"
faces = []
labels = []
label_map = {}
current_label = 0

# ---------------- LOAD DATASET ----------------
for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)
    if not os.path.isdir(person_path):
        continue

    label_map[current_label] = person
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            faces.append(img)
            labels.append(current_label)

    current_label += 1

faces = np.array(faces)
labels = np.array(labels)

# ---------------- TRAIN MODEL ----------------
model = cv2.face.LBPHFaceRecognizer_create()
model.train(faces, labels)

print("Model trained successfully")

# ---------------- CAMERA ----------------
cam = cv2.VideoCapture(0)
time.sleep(1)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- TRACK MARKED STUDENTS ----------------
marked_today = set()
today = datetime.now().strftime("%d-%m-%Y")

# Load already marked names (from CSV)
if os.path.exists("attendance.csv"):
    with open("attendance.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 4 and row[1] == today and row[3] == "Face":
                marked_today.add(row[0])

print("Camera running. Press ESC to stop attendance.")

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cam.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in detected_faces:
        roi = gray[y:y+h, x:x+w]
        label, confidence = model.predict(roi)

        name = label_map[label]
        color = (0, 255, 0)

        if confidence < 80:
            if name not in marked_today:
                time_now = datetime.now().strftime("%H:%M:%S")

                with open("attendance.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, today, time_now, "Face"])

                marked_today.add(name)
                print(f"Attendance marked for {name}")

            cv2.putText(
                frame, f"{name} (Marked)",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
            )
        else:
            cv2.putText(
                frame, "Unknown",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
            )

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    cv2.imshow("Face Attendance - Class Mode", frame)

    # ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
print("Attendance session ended")

# import cv2
# import os
# import numpy as np
# from datetime import datetime
# import csv
# import time

# print("Face attendance (LBPH) started")

# dataset_path = "dataset"
# faces = []
# labels = []
# label_map = {}
# current_label = 0

# # ---------------- LOAD DATASET ----------------
# for person in os.listdir(dataset_path):
#     person_path = os.path.join(dataset_path, person)
#     if not os.path.isdir(person_path):
#         continue

#     label_map[current_label] = person
#     for img_name in os.listdir(person_path):
#         img_path = os.path.join(person_path, img_name)
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is not None:
#             faces.append(img)
#             labels.append(current_label)

#     current_label += 1

# faces = np.array(faces)
# labels = np.array(labels)

# # ---------------- TRAIN MODEL ----------------
# model = cv2.face.LBPHFaceRecognizer_create()
# model.train(faces, labels)

# print("Model trained successfully")

# # ---------------- CAMERA ----------------
# # ⚠️ IMPORTANT: use SAME camera index as QR
# cam = cv2.VideoCapture(0)

# # Give camera time to initialize
# time.sleep(1)

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# print("Camera started, showing preview...")

# while True:
#     ret, frame = cam.read()
#     if not ret:
    #     continue

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # for (x, y, w, h) in detected_faces:
    #     roi = gray[y:y+h, x:x+w]
    #     label, confidence = model.predict(roi)

    #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #     cv2.putText(
    #         frame,
    #         f"{label_map[label]} ({int(confidence)})",
    #         (x, y-10),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.7,
    #         (0, 255, 0),
    #         2
    #     )

    #     # Threshold for recognition
    #     if confidence < 80:
    #         name = label_map[label]
#             date = datetime.now().strftime("%d-%m-%Y")
#             time_now = datetime.now().strftime("%H:%M:%S")

#             with open("attendance.csv", "a", newline="") as f:
#                 writer = csv.writer(f)
#                 writer.writerow([name, date, time_now, "Face"])

#             print(f"Attendance marked for {name}")

#             # Show result briefly before closing
#             cv2.imshow("Face Attendance", frame)
#             cv2.waitKey(1500)

#             cam.release()
#             cv2.destroyAllWindows()
#             exit()

#     # 🔴 THIS LINE IS CRITICAL (WAS THE ISSUE)
#     cv2.imshow("Face Attendance", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cam.release()
# cv2.destroyAllWindows()

# import cv2
# import os
# import numpy as np
# from datetime import datetime
# import csv

# print("Face attendance (LBPH) started")

# dataset_path = "dataset"
# faces = []
# labels = []
# label_map = {}
# current_label = 0

# # Load dataset
# for person in os.listdir(dataset_path):
#     person_path = os.path.join(dataset_path, person)
#     if not os.path.isdir(person_path):
#         continue

#     label_map[current_label] = person
#     for img_name in os.listdir(person_path):
#         img_path = os.path.join(person_path, img_name)
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is not None:
#             faces.append(img)
#             labels.append(current_label)

#     current_label += 1

# faces = np.array(faces)
# labels = np.array(labels)

# # Train model
# model = cv2.face.LBPHFaceRecognizer_create()
# model.train(faces, labels)

# print("Model trained successfully")

# # Start camera
# cam = cv2.VideoCapture(0)

# while True:
#     ret, frame = cam.read()
#     if not ret:
#         continue

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     )

#     detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     for (x, y, w, h) in detected_faces:
#         roi = gray[y:y+h, x:x+w]
#         label, confidence = model.predict(roi)

#         if confidence < 80:
#             name = label_map[label]
#             date = datetime.now().strftime("%d-%m-%Y")
#             time = datetime.now().strftime("%H:%M:%S")

#             with open("attendance.csv", "a", newline="") as f:
#                 writer = csv.writer(f)
#                 writer.writerow([name, date, time, "Face"])

#             print(f"Attendance marked for {name}")
#             cam.release()
#             cv2.destroyAllWindows()
#             exit()

#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#     cv2.imshow("Face Attendance", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cam.release()
# cv2.destroyAllWindows()
