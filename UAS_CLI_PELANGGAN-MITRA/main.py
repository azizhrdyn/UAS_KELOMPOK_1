from utils import clear_screen, press_enter, safe_int, exit_program
from auth import login, register_user, valid_username, valid_password, valid_role, valid_name, load_users
from rekomendasi_makanan import menu_rekomendasi, print_hasil, rekomendasi_terbaik
from olah_makanan import menu_olah_makanan
from manajemen_mitra import lihat_data, tambah_data, hapus_data, update_data, reload_csv
from transaksi import order_makanan
from database_makanan import load_makanan
import pandas as pd

def menu_pelanggan(user):
    while True:
        clear_screen()
        print(f"=== PELANGGAN: {user['nama']} ===")
        print("1. Lihat Profil")
        print("2. Lihat Katalog Makanan")
        print("3. Rekomendasi Makanan")
        print("4. Order Makanan (simulasi)")
        print("0. Logout")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            clear_screen()
            print("=== PROFIL PELANGGAN ===")
            print(f"Nama     : {user['nama']}")
            print(f"Username : {user['username']}")
            print("========================")
            press_enter()
        elif pilih == "2":
            df = load_makanan()
            if df.empty:
                print("\nBelum ada data makanan.")
            else:
                print(df[["nama","restoran","kalori","harga"]].to_string(index=True))
            press_enter()
        elif pilih == "3":
            menu_rekomendasi()
        elif pilih == "4":
            order_makanan()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")
            press_enter()

def menu_mitra(user):
    while True:
        clear_screen()
        print(f"=== MITRA: {user['nama']} ===")
        print("1. Lihat Profil")
        print("2. Lihat Data Makanan (CSV)")
        print("3. Tambah Data Makanan")
        print("4. Hapus Data Makanan")
        print("5. Update Data Makanan")
        print("6. Reload CSV")
        print("7. Olah Data (sorting/searching)")
        print("0. Logout")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            clear_screen()
            print("=== PROFIL MITRA ===")
            print(f"Nama     : {user['nama']}")
            print(f"Username : {user['username']}")
            print("========================")
            press_enter()
        elif pilih == "2":
            lihat_data()
        elif pilih == "3":
            tambah_data()
        elif pilih == "4":
            hapus_data()
        elif pilih == "5":
            update_data()
        elif pilih == "6":
            reload_csv()
        elif pilih == "7":
            menu_olah_makanan()
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid.")
            press_enter()

def menu_admin(user):
    while True:
        clear_screen()
        print(f"=== ADMIN: {user['nama']} ===")
        print("1. Lihat Semua User")
        print("2. Tambah Admin")
        print("0. Logout")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            users = load_users()
            for u, d in users.items():
                print(f"{u} | {d['role']} | {d['nama']}")
            press_enter()

        elif pilih == "2":
            print("\n=== TAMBAH ADMIN ===")
            username = input_username()
            if not username:
                continue
            password = input_password()
            nama = input_nama()

            success = register_user(
                username,
                password,
                "admin",
                nama,
                allow_admin=True
            )

            print("Admin berhasil ditambahkan." if success else "Gagal menambah admin.")
            press_enter()

        elif pilih == "0":
            break

def input_username():
    kesempatan = 3
    for i in range (0,3):
        kesempatan = kesempatan-1
        username = input("Username: ").strip()
        if not username:
            if kesempatan > 0:
                print(f"Username tidak boleh kosong (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        elif not valid_username(username):
            if kesempatan > 0:
                print(f"Username harus alfanumerik (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        else:
            users = load_users()
            if username in users:
                print("Username sudah terdaftar.")
                break
            else:
                return username

def input_password():
    kesempatan = 3
    for i in range (0,3):
        kesempatan = kesempatan-1
        password = input("Password: ").strip()
        if not password:
            if kesempatan > 0:
                print(f"Password tidak boleh kosong (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        elif not valid_password(password):
            if kesempatan > 0:
                print(f"Password minimal 8 karakter dan kombinasi huruf & angka (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        else:
            return password

def input_role():
    kesempatan = 3
    for i in range (0,3):
        kesempatan = kesempatan-1
        role = input("Role (Pelanggan/Mitra): ").strip().lower()
        if not role:
            if kesempatan > 0:
                print(f"Role tidak boleh kosong (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        elif role not in ["pelanggan", "mitra"]:
            if kesempatan > 0:
                print(f"Role harus 'Pelanggan' atau 'Mitra' (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        else:
            return role

def input_nama():
    kesempatan = 3
    for i in range (0,3):
        kesempatan = kesempatan-1
        nama = input("Nama lengkap: ").strip()
        if not nama:
            if kesempatan > 0:
                print(f"Password tidak boleh kosong (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        elif not valid_name(nama):
            if kesempatan > 0:
                print(f"Nama harus mengandung huruf (sisa kesempatan: {kesempatan}).")
            else:
                print("Registrasi gagal.")
        else:
            return nama

def main():
    while True:
        clear_screen()
        print("=== FLAVOR OF ONE DAY (CLI) ===")
        print("1. Login")
        print("2. Register")
        print("0. Keluar")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            user = login()
            if user:
                if user["role"] == "pelanggan":
                    menu_pelanggan(user)
                elif user["role"] == "mitra":
                    menu_mitra(user)
                elif user["role"] == "admin":
                    menu_admin(user)

        elif pilih == "2":
            clear_screen()
            print("=== REGISTER USER ===")

            while True:
                username = input_username() 
                if not username:
                    break
                password = input_password()
                if not password:
                    break
                role = input_role()
                if not role:
                    break
                nama = input_nama()
                if not nama:
                    break

                success = register_user(username, password, role, nama)
                if success:
                    print("Registrasi berhasil. Silakan login.")
                    break
            press_enter()

        elif pilih == "0":
            exit_program()
        else:
            print("Pilihan tidak valid.")
            press_enter()

if __name__ == "__main__":
    main()



