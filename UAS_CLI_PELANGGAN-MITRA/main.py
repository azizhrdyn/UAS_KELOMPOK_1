from utils import clear_screen, press_enter, safe_int, exit_program
from auth import login, register_demo
from rekomendasi_makanan import menu_rekomendasi, print_hasil, rekomendasi_terbaik
from olah_makanan import menu_olah_makanan
from manajemen_mitra import lihat_data, tambah_data, hapus_data, update_data, reload_csv
from pembayaran import simulasi_pembayaran
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
            print(f"\nProfil: {user}")
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
            df = load_makanan()
            if df.empty:
                print("Belum ada makanan.")
                press_enter()
                continue
            print(df[["nama","restoran","kalori","harga"]].to_string(index=True))
            pilih_idx = input("Masukkan index makanan yang ingin dipesan (pisah koma untuk beberapa): ").strip()
            if not pilih_idx:
                continue
            try:
                indices = [int(x.strip()) for x in pilih_idx.split(",")]
            except:
                print("Input index tidak valid.")
                press_enter()
                continue
            order_lines = []
            total = 0
            for idx in indices:
                if idx in df.index:
                    qty = safe_int(input(f"Jumlah untuk '{df.at[idx,'nama']}' : "), 1)
                    harga = int(df.at[idx,'harga'])
                    subtotal = harga * qty
                    order_lines.append((df.at[idx,'nama'], df.at[idx,'restoran'], qty, harga, subtotal))
                    total += subtotal
                else:
                    print("Index", idx, "tidak ada, diabaikan.")
            if not order_lines:
                print("Tidak ada item valid dipesan.")
                press_enter()
                continue
            
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





