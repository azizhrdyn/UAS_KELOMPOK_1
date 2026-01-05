from auth import load_users, register_user, set_user_status, delete_user, valid_name, valid_password, valid_username
from database_makanan import load_makanan, save_makanan, tambah_makanan, hapus_makanan
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
            clear_screen()
            print("=== NONAKTIFKAN/AKTIFKAN USER ===")
            
            for kesempatan in range(3):
                u = input("Masukkan Username: ").strip()
                if u:
                    user = load_users().get(u)
                    if user:
                        new_status = "nonaktif" if user["status"] == "aktif" else "aktif"
                        set_user_status(u, new_status)
                        print(f"User '{u}' telah di{new_status}kan.")
                        press_enter()
                        break
                    else:
                        print(f"Username '{u}' tidak ditemukan, coba lagi. (sisa kesempatan: {2 - kesempatan})")
                elif not u:
                    print(f"Username tidak boleh kosong, coba lagi. (sisa kesempatan: {2 - kesempatan})")
                    user = None
                if kesempatan == 2:
                    print("Pengubahan status user dibatalkan.")
                    press_enter()
                    return
            
        elif pilih == "2":
            clear_screen()
            print("=== HAPUS USER ===")
            
            for kesempatan in range(3):
                u = input("Masukkan Username: ").strip()
                user = load_users().get(u)
                if u in users:
                    confirm = input(f"Yakin hapus user '{u}'? (y/n): ").strip().lower()
                    if confirm == "y":
                        delete_user(u)
                        print(f"User '{u}' telah dihapus.")
                        press_enter()
                        return
                    elif confirm == "n":
                        print("Hapus user dibatalkan.")
                        press_enter()
                        return
                    else:
                        print(f"Input tidak valid, coba lagi (sisa kesempatan: {2 - kesempatan}).")
                elif u == "":
                    print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                elif not user:
                    print(f"Username '{u}' tidak ditemukan (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Hapus user dibatalkan.")
                    press_enter()
                    return

        elif pilih == "3":
            while True:
                clear_screen()
                
                print("=== TAMBAH ADMIN BARU ===")
                for kesempatan in range(3):
                    username = input("Username: ").strip()
                    if not username:
                        print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                    elif not valid_username(username):
                        print(f"Username harus alfanumerik dan minimal terdiri dari 4 karakter (sisa kesempatan: {2 - kesempatan}).")
                    elif username in users:
                        print(f"Username sudah terdaftar (sisa kesempatan: {2 - kesempatan}).")
                    else:
                        break 
                    if kesempatan == 2:
                        print("Registrasi gagal.")
                        press_enter()
                        return
                    
                for kesempatan in range(3):
                    password = input("Password: ").strip()
                    if not password:
                        print(f"Password tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                    elif not valid_password(password):
                        print(f"Password minimal 8 karakter dan kombinasi huruf & angka (sisa kesempatan: {2 - kesempatan}).")
                    else:
                        break
                    if kesempatan == 2:
                        print("Registrasi gagal.")
                        press_enter()
                        return
                    
                for kesempatan in range(3):
                    nama = input("Nama: ").strip()
                    if not nama:
                        print(f"Nama tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                    elif not valid_name(nama):
                        print(f"Nama hanya boleh mengandung alfabet dan spasi (sisa kesempatan: {2 - kesempatan}).")
                    else:
                        break
                    if kesempatan == 2:
                        print("Registrasi gagal.")
                        press_enter()
                        return

                register_user(username, password, "admin", nama, allow_admin=True)
                print("Admin baru berhasil ditambahkan.")
                press_enter()
                break

        elif pilih == "0":
            break
        

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
            clear_screen()
            print("=== TAMBAH MAKANAN BARU ===")
            
            for kesempatan in range(3):
                restoran = input("Nama Restoran: ").strip()
                if not restoran:
                    print(f"Nama restoran tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    break   
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return
                
            for kesempatan in range(3):
                nama = input("Nama Makanan: ").strip()
                if nama not in df[df["restoran"] == restoran]["nama"].values:
                    break
                elif nama == "":
                    print(f"Nama makanan tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    print(f"Makanan '{nama}' di restoran '{restoran}' sudah ada! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return

            for kesempatan in range(3):
                kalori = input("Kalori: ").strip()
                if kalori == "":
                    print(f"Kalori tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    try:
                        kalori = int(kalori)
                        if kalori < 0:
                            print(f"Kalori tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                        elif kalori == 0:
                            print(f"Kalori harus lebih dari nol! (sisa kesempatan: {2 - kesempatan})")
                        else:
                            break
                    except ValueError:
                        print(f"Kalori harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return
                      
            for kesempatan in range(3):
                harga = input("Harga: ").strip()
                if harga == "":
                    print(f"Harga tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    try:
                        harga = int(harga)
                        if harga < 0:
                            print(f"Harga tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                        elif harga == 0:
                            print(f"Harga harus lebih dari nol! (sisa kesempatan: {2 - kesempatan})")
                        else:
                            break
                    except ValueError:
                        print(f"Harga harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return
                        
            for kesempatan in range(3):
                stok = input("Stok: ").strip()
                if stok == "":
                    print(f"Stok tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                elif stok.isdigit():
                    stok = int(stok)
                    if stok < 0:
                        print(f"Stok minimal 0! (sisa kesempatan: {2 - kesempatan})")
                    else:
                        break
                elif not stok.isdigit():
                    print(f"Stok harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return

            tambah_makanan(nama, restoran, kalori, harga, stok)
            print("Makanan baru berhasil ditambahkan.")
            press_enter()

        elif pilih == "2":
            clear_screen()
            print("=== UPDATE DATA MAKANAN ===")
            
            for kesempatan in range(3):
                idx = input("Index makanan: ").strip()
                if not idx:
                    print(f"Index tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                else:
                    try:
                        idx = int(idx) - 1
                        if idx < 0 or idx >= len(df):
                            print(f"Index tidak ditemukan (sisa kesempatan: {2 - kesempatan}).")
                        else:   
                            data_lama = df.loc[idx]
                            nama_lama = data_lama["nama"]
                            restoran_lama = data_lama["restoran"]
                            break
                    except ValueError:
                        print(f"Index tidak valid, masukkan angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Update data makanan dibatalkan.")
                    press_enter()
                    return
                
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
                if kalori == "":
                    print(f"Kalori tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    try:
                        kalori = int(kalori)
                        if kalori < 0:
                            print(f"Kalori tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                        elif kalori == 0:
                            print(f"Kalori harus lebih dari nol! (sisa kesempatan: {2 - kesempatan})")
                        else:
                            break
                    except ValueError:
                        print(f"Kalori harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return
                
            for kesempatan in range(3):
                harga = input("Harga baru: ").strip()
                if harga == "":
                    print(f"Harga tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    try:
                        harga = int(harga)
                        if harga < 0:
                            print(f"Harga tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                        elif harga == 0:
                            print(f"Harga harus lebih dari nol! (sisa kesempatan: {2 - kesempatan})")
                        else:
                            break
                    except ValueError:
                        print(f"Harga harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return

            for kesempatan in range(3):
                stok = input("Stok baru: ").strip()
                if stok == "":
                    print(f"Stok tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                elif stok.isdigit():
                    stok = int(stok)
                    if stok < 0:
                        print(f"Stok minimal 0! (sisa kesempatan: {2 - kesempatan})")
                    else:
                        break
                elif not stok.isdigit():
                    print(f"Stok harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return
            
            def update_makanan(idx, nama=None, restoran=None, kalori=None, harga=None, stok=None):
                df = load_makanan()
                if idx not in df.index:
                    return
                else:
                    idx = int(idx)
                if nama is not None:
                    df.at[idx, "nama"] = nama
                if restoran is not None:
                    df.at[idx, "restoran"] = restoran
                if kalori is not None:
                    df.at[idx, "kalori"] = kalori
                if harga is not None:
                    df.at[idx, "harga"] = harga
                if stok is not None:
                    df.at[idx, "stok"] = stok
                save_makanan(df)

            update_makanan(idx, nama=nama_final, restoran=restoran_final, kalori=kalori, harga=harga, stok=stok)
            print("Makanan berhasil diperbarui.")
            press_enter()

        elif pilih == "3":
            clear_screen()
            print("=== HAPUS DATA MAKANAN ===")
            
            for kesempatan in range(3):
                idx = input("Index makanan: ").strip()
                if idx == "":
                    print(f"Index tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                else:
                    try:
                        idx = int(idx) - 1
                        if idx < 0 or idx >= len(df):
                            print(f"Index tidak ditemukan (sisa kesempatan: {2 - kesempatan}).")
                        else:   
                            df = df.drop(idx).reset_index(drop=True)
                            save_makanan(df)
                            print("Makanan berhasil dihapus")
                            press_enter()
                            break
                    except ValueError:
                        print(f"Index tidak valid, masukkan angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Update data makanan dibatalkan.")
                    press_enter()
                    return

        elif pilih == "0":
            break


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
