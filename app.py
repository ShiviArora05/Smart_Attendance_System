from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import csv
import sys


app = Flask(__name__)
app.secret_key = "smart-attendance-secret-key"

# ---------------- USERS WITH ROLES ----------------
USERS = {
    "admin":   {"password": "admin123",  "role": "admin"},
    "shivi":   {"password": "shivi@123",  "role": "admin"},
    "viewer1": {"password": "viewer123",  "role": "viewer"}
}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username]["password"] == password:
            session["user"] = username
            session["role"] = USERS[username]["role"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


# ---------------- FACE ATTENDANCE (ADMIN ONLY) ----------------
# @app.route("/face")
# def face_attendance():
#     if session.get("role") != "admin":
#         return "Access Denied"

#     subprocess.Popen(["python", "face_attendance.py"])
#     return render_template("success.html")


# # ---------------- QR ATTENDANCE (ADMIN ONLY) ----------------
# @app.route("/qr")
# def qr_attendance():
#     if session.get("role") != "admin":
#         return "Access Denied"

#     subprocess.Popen(["python", "qr_attendance.py"])
#     return render_template("success.html")
@app.route("/face")
def face_attendance():
    if session.get("role") != "admin":
        return "Access Denied"

    subprocess.Popen([sys.executable, "face_attendance.py"])
    return render_template("success.html")


@app.route("/qr")
def qr_attendance():
    if session.get("role") != "admin":
        return "Access Denied"

    subprocess.Popen([sys.executable, "qr_attendance.py"])
    return render_template("success.html")



# ---------------- VIEW ATTENDANCE (ADMIN + VIEWER) ----------------
@app.route("/attendance")
def view_attendance():
    if "role" not in session:
        return redirect(url_for("login"))

    records = []
    try:
        with open("attendance.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            records = list(reader)
    except FileNotFoundError:
        pass

    return render_template("attendance.html", records=records)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

    # app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, session
# import subprocess
# import csv
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "smart-attendance-secret"

# USERS = {
#     "admin": {"password": "admin123", "role": "admin"},
#     "shivi": {"password": "shivi@123", "role": "admin"},
#     "viewer1": {"password": "viewer123", "role": "viewer"}
# }



# # ---------------- LOGIN ----------------
# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user = request.form["username"]
#         pwd = request.form["password"]

#         if user in USERS and USERS[user]["password"] == pwd:
#             session["user"] = user
#             session["role"] = USERS[user]["role"]
#         return redirect(url_for("dashboard"))
#     else:
#         return render_template("login.html", error="Invalid credentials")
 
 

#     # return render_template("login.html")


# @app.route("/logout")
# def logout():
#     session.pop("admin", None)
#     return redirect(url_for("login"))

# # ---------------- DASHBOARD ----------------
# @app.route("/dashboard")
# def dashboard():
#     if not session.get("admin"):
#         return redirect(url_for("login"))
#     return render_template("index.html")

# # ---------------- ATTENDANCE ----------------
# @app.route("/face")
# def face():
#     # if not session.get("admin"):
#     #     return redirect(url_for("login"))
#     # subprocess.Popen(["python", "face_attendance.py"])
#     # return render_template("success.html")
#     if session.get("role") != "admin":
#         return "Access Denied"
#     subprocess.Popen(["python", "face_attendance.py"])
#     return render_template("success.html")

# @app.route("/qr")
# def qr():
#     # if not session.get("admin"):
#     #     return redirect(url_for("login"))
#     # subprocess.Popen(["python", "qr_attendance.py"])
#     # return render_template("success.html")
#     if session.get("role") != "admin":
#         return "Access Denied"
#     subprocess.Popen(["python", "qr_attendance.py"])
#     return render_template("success.html")

# # ---------------- VIEW ATTENDANCE ----------------
# @app.route("/attendance")
# def attendance():
#     # if not session.get("admin"):
#     #     return redirect(url_for("login"))

#     # records = []
#     # try:
#     #     with open("attendance.csv", "r") as f:
#     #         reader = csv.reader(f)
#     #         next(reader)
#     #         records = list(reader)
#     # except FileNotFoundError:
#     #     pass

#     # return render_template("attendance.html", records=records)
#      if "role" not in session:
#         return redirect(url_for("login"))
#      records = []
#      with open("attendance.csv") as f:
#         reader = csv.reader(f)
#         next(reader)
#         records = list(reader)
#     return render_template("attendance.html", records=records)

# if __name__ == "__main__":
#     app.run(debug=True)
