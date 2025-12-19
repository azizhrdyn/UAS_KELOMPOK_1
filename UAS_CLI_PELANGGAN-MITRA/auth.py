import csv
import os

FILE_USER = "user.csv"

def load_users():
    users = {}

    if not os.path.exists(FILE_USER):
        return users

    with open(FILE_USER, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"],
                "nama": row["nama"]
            }
    return users

def login():
    print("=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    users = load_users()
    user = users.get(username)

    if not user:
        print("Login gagal: username tidak ditemukan.")
        return None

    if password != user["password"]:
        print("Login gagal: password salah.")
        return None

    print(f"Login berhasil. Selamat datang, {user['nama']}!")
    return {
    "username": username,
    "password": user["password"],
    "role": user["role"],
    "nama": user["nama"]
    }

def register_user(username, password, role, nama, allow_admin=False):
    users = load_users()

    if username in users:
        return False

    if role == "admin" and not allow_admin:
        return False

    with open(FILE_USER, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(["username", "password", "role", "nama"])

        writer.writerow([username, password, role, nama])

    return True

def valid_username(username):
    return username.isalnum()

def valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

def valid_role(role):
    return role in ["pelanggan", "mitra", "admin"]

def valid_name(nama):
    return any(c.isalpha() for c in nama)

