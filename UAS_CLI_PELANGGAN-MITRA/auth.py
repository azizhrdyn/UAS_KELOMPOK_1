USERS = {
    "alice": {"password": "alice123", "role": "pelanggan", "nama": "Alice Pelanggan"},
    "budi":  {"password": "budi123",  "role": "mitra",      "nama": "Budi Mitra"},
    "tina":  {"password": "tina123",  "role": "pelanggan", "nama": "Tina Pelanggan"},
}

def login():
    print("=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Login berhasil. Halo, {user['nama']} ({user['role']})")
        return {"username": username, "role": user["role"], "nama": user["nama"]}
    print("Login gagal — username/password salah.")
    return None

def register_demo(username, password, role="pelanggan", nama=None):
    if username in USERS:
        return False
    USERS[username] = {"password": password, "role": role, "nama": nama or username}
    if role not in ["pelanggan", "mitra"]:
        print("Role tidak valid, harus 'pelanggan' atau 'mitra'.")
        return False
    return True
