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

def main():
    while True:
        clear_screen()
        print("=== FLAVOR OF ONE DAY (CLI) ===")
        print("1. Login")
        print("2. Register demo user (opsional)")
        print("0. Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            user = login()
            if user:
                if user["role"] == "pelanggan":
                    menu_pelanggan(user)
                elif user["role"] == "mitra":
                    menu_mitra(user)
        elif pilih == "2":
            print("Register: buat user baru.")
            u = input("Username baru: ").strip()
            p = input("Password: ").strip()
            role = input("Role (pelanggan/mitra): ").strip() or "pelanggan"
            nama = input("Nama lengkap: ").strip() or u
            ok = register_demo(u,p,role,nama)
            if ok:
                print("User berhasil terdaftar. Gunakan menu Login.")
            else:
                print("Username sudah ada.")
            press_enter()
        elif pilih == "0":
            exit_program()
        else:
            print("Pilihan tidak valid.")
            press_enter()

