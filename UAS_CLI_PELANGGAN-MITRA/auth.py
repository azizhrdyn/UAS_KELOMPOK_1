import csv
import os
from utils import press_enter

FILE_USER = "user.csv"
TOKO_FILE = "profil_toko.csv"

FIELDNAMES = ["username", "password", "role", "nama", "toko", "status"]

def ensure_user_csv():
    if not os.path.exists(FILE_USER):
        with open(FILE_USER, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDNAMES)

def load_users():
    ensure_user_csv()
    users = {}
    with open(FILE_USER, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"],
                "nama": row["nama"],
                "toko": row.get("toko", ""),
                "status": row.get("status", "aktif")
            }
    return users

def save_all_users(users):
    with open(FILE_USER, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for u, d in users.items():
            writer.writerow({
                "username": u,
                "password": d["password"],
                "role": d["role"],
                "nama": d["nama"],
                "toko": d.get("toko", ""),
                "status": d.get("status", "aktif")
            })

def input_username():
    for kesempatan in range(3):
        username = input("Username: ").strip()
        if not username:
            print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_username(username):
            print(f"Username harus alfanumerik dan minimal terdiri dari 4 karakter (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif username in load_users():
            print(f"Username sudah terdaftar (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return username

def input_password():
    for kesempatan in range(3):
        password = input("Password: ").strip()
        if not password:
            print(f"Password tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_password(password):
            print(f"Password minimal 8 karakter dan kombinasi huruf & angka (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return password

def input_role():
    for kesempatan in range(3):
        role = input("Role (pelanggan/mitra): ").strip().lower()
        if not role:
            print(f"Role tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_role(role) or role == "admin":
            print(f"Role harus 'pelanggan' atau 'mitra' (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return role
        
def input_nama():
    for kesempatan in range(3):
        nama = input("Nama: ").strip()
        if not nama:
            print(f"Nama tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_name(nama):
            print(f"Nama hanya boleh mengandung alfabet dan spasi (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return nama

def input_toko():
    for kesempatan in range(3):
        toko = input("Toko: ").strip()
        if not toko:
            print(f"Toko tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_name(toko):
            print(f"Toko hanya boleh mengandung alfabet dan spasi (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return toko

def login():
    while True:
        load_users()
        print("=== LOGIN ===")
        for kesempatan in range(3):
            username = input("Username: ").strip()
            if username == "":
                print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            elif username not in load_users():
                print(f"Username tidak ditemukan (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            else:
                break
        
        for kesempatan in range(3):
            user = load_users().get(username)
            password = input("Password: ").strip()
            if not password:
                print(f"Password tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            elif password != user["password"]:
                print(f"Password salah (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            else:
                break

        if not user:
            print("Login gagal: username tidak ditemukan.")
            return None

        if password != user["password"]:
            print("Login gagal: password salah.")
            return None

        if user["status"] != "aktif":
            print("Akun nonaktif.")
            press_enter()
            return None

        print(f"Login berhasil. Selamat datang, {user['nama']}!")
        return {
            "username": username,
            "password": user["password"],
            "role": user["role"],
            "nama": user["nama"],
            "toko": user.get("toko", ""),
            "status": user.get("status", "aktif")
        }

def register_user(username, password, role, nama, toko="", allow_admin=False):
    users = load_users()

    if username in users:
        return False

    if role == "admin" and not allow_admin:
        return False
        
    print("Register berhasil, silakan Login.")
    users[username] = {
        "password": password,
        "role": role,
        "nama": nama,
        "toko": toko,
        "status": "aktif"
    }

    save_all_users(users)
    return True


# Fungsi buat edit profil pengguna 
def get_profil_dasar(username):
    with open("user.csv", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == username:
                return {
                    "username": data[0],
                    "nama": data[3]
                }

def get_profil_lengkap(username):
    with open("user.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return {
                    "email": row.get("email", ""),
                    "no_hp": row.get("no_hp", ""),
                    "alamat": row.get("alamat", ""),
                    "jenis_kelamin": row.get("jenis_kelamin", "")
                }

def edit_profil_lengkap(username, profil_baru):
    rows = []

    fieldnames = [
        "username",
        "password",
        "role",
        "nama",
        "toko",
        "status",
        "email",
        "no_hp",
        "alamat",
        "jenis_kelamin"
    ]

    with open("user.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                for key in profil_baru:
                    row[key] = profil_baru[key]
            rows.append(row)

    with open("user.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
            
def get_user_by_username(username):
    with open("user.csv", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == username:
                return {
                    "username": data[0],
                    "password": data[1],
                    "role": data[2],
                    "nama": data[3],
                    "toko": data[4],
                    "status": data[5]
                }


# Fungsi buat edit profil mitra
def get_profil_toko(username):
    if not os.path.exists(TOKO_FILE):
        return {
            "lokasi": "",
            "jam_operasional": "",
            "deskripsi": ""
        }

    with open(TOKO_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return row

    return {
        "lokasi": "",
        "jam_operasional": "",
        "deskripsi": ""
    }


def edit_profil_toko(username, data_baru):
    rows = []
    found = False

    if os.path.exists(TOKO_FILE):
        with open(TOKO_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username:
                    row.update(data_baru)
                    found = True
                rows.append(row)

    if not found:
        rows.append({
            "username": username,
            **data_baru
        })

    with open(TOKO_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["username", "lokasi", "jam_operasional", "deskripsi"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def set_user_status(username, status):
    users = load_users()
    if username not in users:
        return False
    users[username]["status"] = status
    save_all_users(users)
    return True

def delete_user(username):
    users = load_users()
    if username not in users:
        return False
    del users[username]
    save_all_users(users)
    return True

def valid_username(username):
    return len(username) >= 4 and any(c.isalnum() for c in username) and any(c.isalpha() for c in username)

def valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

def valid_role(role):
    return role in ["pelanggan", "mitra", "admin"]

def valid_name(nama):
    return any(c.isalpha() for c in nama)
    
def valid_email(email):
    allowed_domains = (
        "@gmail.com",
        "@yahoo.com",
        "@outlook.com",
        "@hotmail.com",
        "@icloud.com"
    )
    return email.endswith(allowed_domains)
