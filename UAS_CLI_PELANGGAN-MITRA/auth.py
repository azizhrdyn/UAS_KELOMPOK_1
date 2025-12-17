USERS = {
    "alice": {"password": "alice123", "role": "pelanggan", "nama": "Alice Pelanggan"},
    "budi":  {"password": "budi123",  "role": "mitra",      "nama": "Budi Mitra"},
    "tina":  {"password": "tina123",  "role": "pelanggan", "nama": "Tina Pelanggan"},
}

def login():
    print("=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if not username or not password:
        print("Login gagal: username dan password wajib diisi.")
        return None

    user = USERS.get(username)

    if user is None:
        print("Login gagal: username tidak terdaftar.")
        return None
    if user["password"] != password:
        print("Login gagal: password salah.")
        return None
    print(f"Login berhasil. Halo, {user['nama']} ({user['role']})")
    return {
        "username": username,
        "role": user["role"],
        "nama": user["nama"]
    }

def valid_username(username):
    return bool(username) and username.isalnum()

def valid_name(nama):
    return bool(nama) and any(c.isalpha() for c in nama)

def valid_role(role):
    return role in ["pelanggan", "mitra"]

def valid_password(password):
    if len(password) < 8:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True
    
def register_user(username, password, role, nama):
    if not username or not password or not role or not nama:
        print("Register gagal: semua field wajib diisi.")
        return False

    if not username.isalnum():
        print("Register gagal: username harus alfanumerik.")
        return False
        
    if not any(c.isalpha() for c in nama):
        print("Register gagal: nama tidak valid.")
        return False

    if role not in ["pelanggan", "mitra"]:
        print("Register gagal: role tidak valid.")
        return False

    if username in USERS:
        print("Register gagal: username sudah terdaftar.")
        return False

    if not valid_password(password):
        print("Register gagal: password minimal 8 karakter dan kombinasi huruf & angka.")
        return False

    USERS[username] = {
        "password": password,
        "role": role,
        "nama": nama
    }
    return True
