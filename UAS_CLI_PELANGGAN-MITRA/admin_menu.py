from auth import load_users, register_user, set_user_status, delete_user, valid_name, valid_password, valid_username
from database_makanan import load_makanan, save_makanan, tambah_makanan, update_makanan, hapus_makanan
from utils import press_enter, clear_screen
import os
import pandas as pd
from pathlib import Path

BACKUP_MAKANAN = Path("backup_makanan.csv")
BACKUP_USER = Path("backup_user.csv")


def manajemen_user():
    while True:
        clear_screen()
        users = load_users()
        df = (pd.DataFrame.from_dict(users, orient="index").reset_index().rename(columns={"index": "username"}))
        print(df[["username","nama","role","toko","status"]].assign(no=range(1, len(df) + 1))[["no","username","nama","role","toko","status"]].to_string(index=False))
        
        print("\n1. Nonaktifkan/Aktifkan User")
        print("2. Hapus User")
        print("3. Tambah Admin")
        print("0. Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            u = input("Username: ").strip()
            user = load_users().get(u)
            if user:
                new_status = "nonaktif" if user["status"] == "aktif" else "aktif"
                set_user_status(u, new_status)
            press_enter()

        elif pilih == "2":
            while True:
                u = input("Masukkan username (atau 0 untuk batal): ").strip()
                user = load_users().get(u)
                if u in users:
                    confirm = input(f"Yakin hapus user '{u}'? (y/n): ").strip().lower()
                    if confirm == "y":
                        delete_user(u)
                        print(f"User '{u}' telah dihapus.")
                        press_enter()
                        return
                    else:
                        print("Hapus user dibatalkan.")
                    break
                elif u == "":
                    print("Username tidak boleh kosong.")
                elif u == "0":
                    print("Hapus user dibatalkan.")
                    press_enter()
                    break
                elif not user:
                    print("Username tidak ditemukan.")

        elif pilih == "3":
            while True:
                
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
                    elif username in users:
                        print(f"Username sudah terdaftar (sisa kesempatan: {2 - kesempatan}).")
                        if kesempatan == 2:
                            print("Registrasi gagal.")
                            press_enter()
                            return
                    else:
                        break
                    
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
                        break
                    
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
                        break

                register_user(username, password, "admin", nama, allow_admin=True)
                print("Admin baru berhasil ditambahkan.")
                press_enter()
                break

        elif pilih == "0":
            break

        else:
            press_enter()

def manajemen_data():
    while True:
        clear_screen()
        df = load_makanan()
        print(df[["nama","restoran","kalori","harga","stok"]].assign(no=range(1, len(df) + 1))[["no","nama","restoran","kalori","harga","stok"]].to_string(index=False))

        print("\n1. Tambah Makanan")
        print("2. Update Makanan")
        print("3. Hapus Makanan")
        print("0. Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            for kesempatan in range(3):
                nama = input("Nama: ").strip()
                if nama:
                    break
                else:
                    print(f"Nama makanan tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan == 2:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return

            for kesempatan in range(3):
                restoran = input("Restoran: ").strip()
                if not restoran:
                    print(f"Nama restoran tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    duplikat = df[
                        (df["nama"].str.lower() == nama.lower()) &
                        (df["restoran"].str.lower() == restoran.lower())
                    ]
            
                    if not duplikat.empty:
                        print(
                            f"Makanan '{nama}' di restoran '{restoran}' sudah ada "
                            f"(sisa kesempatan: {2 - kesempatan})"
                        )
                    else:
                        break
            
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return

            for kesempatan in range(3):
                kalori = input("Kalori: ").strip()
                if kalori:
                    break
                else:
                    print(f"Kalori tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        kalori = input("Kalori: ").strip()
                    else:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return
      
            for kesempatan in range(3):
                harga = input("Harga: ").strip()
                if harga:
                    break
                else:
                    print(f"Harga tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        harga = input("Harga: ").strip()
                    else:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return
                        
            for kesempatan in range(3):
                stok = input("Stok: ").strip()
                if stok:
                    break
                else:
                    print(f"Stok tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        stok = input("Stok: ").strip()
                    else:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return

            if kalori.isdigit() and harga.isdigit() and stok.isdigit():
                kalori = int(kalori)
                harga = int(harga)
                stok = int(stok)
                tambah_makanan(nama, restoran, kalori, harga, stok)
            press_enter()

        elif pilih == "2":
            idx = input("Index makanan: ").strip()
        
            if not idx.isdigit():
                print("Index tidak valid, masukkan angka.")
                press_enter()
                continue
        
            idx = int(idx) - 1
        
            if idx < 0 or idx >= len(df):
                print("Index tidak ditemukan.")
                press_enter()
                continue
                
            data_lama = df.loc[idx]
            nama_lama = data_lama["nama"]
            restoran_lama = data_lama["restoran"]
                
            for kesempatan in range(3):
                nama_input = input("Nama baru (kosongkan jika tidak diubah): ").strip()
                nama_final = nama_input if nama_input else nama_lama
                break
              
            for kesempatan in range(3):
                restoran_input = input("Restoran baru (kosongkan jika tidak diubah): ").strip()
                restoran_final = restoran_input if restoran_input else restoran_lama
                
                duplikat = df[
                    (df["nama"] == nama_final) &
                    (df["restoran"] == restoran_final) &
                    (df.index != idx)
                ]
                
                if not duplikat.empty:
                    print(f"Makanan '{nama_final}' di restoran '{restoran_final}' sudah ada! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        continue
                    else:
                        print("Update makanan dibatalkan.")
                        press_enter()
                        return
                break
                    
            for kesempatan in range(3):
                kalori = input("Kalori baru: ").strip()
                if kalori.isdigit():
                    kalori = int(kalori)
                    break
                else:
                    print(f"Kalori harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan == 2:
                        print("Update makanan dibatalkan.")
                        press_enter()
                        return
                
            for kesempatan in range(3):
                harga = input("Harga baru: ").strip()
                if harga.isdigit():
                    harga = int(harga)
                    break
                else:
                    print(f"Harga harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan == 2:
                        print("Update makanan dibatalkan.")
                        press_enter()
                        return

            for kesempatan in range(3):
                stok = input("Stok baru: ").strip()
                if stok.isdigit():
                    stok = int(stok)
                    break
                else:
                    print(f"Stok harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan == 2:
                        print("Update makanan dibatalkan.")
                        press_enter()
                        return
            
            update_makanan(
            idx,
            nama=nama_final,
            kalori=kalori,
            harga=harga,
            stok=stok
            )
            press_enter()

        elif pilih == "3":
            idx = input("Index makanan: ").strip()
            
            if not idx.isdigit():
                print("Index tidak valid, masukkan angka.")
                press_enter()
                continue
        
            idx = int(idx) - 1
        
            if idx < 0 or idx >= len(df):
                print("Index tidak ditemukan.")
                press_enter()
                continue
            
            df = df.drop(idx).reset_index(drop=True)
            save_makanan(df)
            press_enter()

        elif pilih == "0":
            break

        else:
            press_enter()

def kontrol_sistem():
    while True:
        clear_screen()
        print("1. Backup Data")
        print("2. Restore Data")
        print("0. Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            clear_screen()
            print("Membackup data", end="", flush=True)
            for i in range(3):
                print(".", end="", flush=True)
                import time
                time.sleep(1) 
            print("\nBackup selesai.")           
            press_enter()
            return
        
        elif pilih == "2":
            clear_screen()
            print("Merestore data", end="", flush=True)
            for i in range(3):
                print(".", end="", flush=True)
                import time
                time.sleep(1) 
            print("\nRestore selesai.")           
            press_enter()
            return

        elif pilih == "0":
            break

        else:
            clear_screen()

def menu_admin(user):
    while True:
        clear_screen()
        print(f"=== ADMIN: {user['nama']} ===")
        print("1. Manajemen User")
        print("2. Manajemen Data Makanan")
        print("3. Kontrol Sistem")
        print("0. Logout")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            manajemen_user()

        elif pilih == "2":
            manajemen_data()

        elif pilih == "3":
            kontrol_sistem()

        elif pilih == "0":
            break

        else:
            press_enter()
