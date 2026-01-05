from database_makanan import load_makanan, save_makanan, tambah_makanan, update_makanan, hapus_makanan
from utils import press_enter, clear_screen
import csv
from pathlib import Path
from auth import get_profil_toko, edit_profil_toko
import re

PENJUALAN_CSV = Path("penjualan.csv")

def profil_toko(user):
    clear_screen()
    profil = get_profil_toko(user["username"])
    
    print("=== PROFIL TOKO ===")
    print(f"Nama Toko : {user['toko']}")
    print(f"Pemilik   : {user['nama']}")

    if profil["lokasi"]:
        print(f"Lokasi          : {profil['lokasi']}")
        print(f"Jam Operasional : {profil['jam_operasional']}")
        if profil["deskripsi"]:
            print(f"Deskripsi       : {profil['deskripsi']}")

    print("\n1. Lengkapi / Edit Profil Toko")
    print("2. Kembali")
    sub = input("Pilih: ").strip()

    if sub == "1":
        clear_screen()
        print("=== EDIT PROFIL TOKO ===")


        lokasi = input(f"Lokasi [{profil['lokasi']}]: ") or profil["lokasi"]

        percobaan = 0
        batal = False

        while percobaan < 3:
            jam_input = input(f"Jam Operasional [{profil['jam_operasional']}]: ") or profil["jam_operasional"]

            if re.match(r"^\d{2}\.\d{2} - \d{2}\.\d{2}$", jam_input):
                jam = jam_input
                break
            else:
                percobaan += 1
                print(f"Format jam salah! Gunakan hh.mm - hh.mm (sisa {3 - percobaan} kesempatan)")

        else:
            print("\nGagal memperbarui jam operasional. Kembali ke menu profil.")
            press_enter()
            return

        desk = input(f"Deskripsi [{profil['deskripsi']}]: ") or profil["deskripsi"]

        edit_profil_toko(user["username"], {
            "lokasi": lokasi,
            "jam_operasional": jam_input,
            "deskripsi": desk
        })

        print("\nProfil toko berhasil diperbarui.")
    press_enter()

def kelola_menu(user):
    while True:
        clear_screen()
        df = load_makanan().reset_index(drop=True)
        toko_df = df[df["restoran"] == user["toko"]].copy()
        toko_df["__idx"] = toko_df.index
        toko_df = toko_df.reset_index(drop=True)

        print(toko_df[["nama","kalori","harga","stok"]].assign(no=range(1, len(toko_df) + 1))[["no","nama","kalori","harga","stok"]].to_string(index=False))
        print("\n1. Tambah Menu")
        print("2. Update Menu")
        print("3. Hapus Menu")
        print("0. Kembali")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            
            nama = input("Nama makanan: ").strip()
            for kesempatan in range(3):
                if nama:
                    if nama.lower() in toko_df["nama"].str.lower().values:
                        print(f"Nama makanan '{nama}' sudah ada di toko Anda! (sisa kesempatan: {2 - kesempatan})")
                        if kesempatan < 2:
                            nama = input("Nama makanan: ").strip()
                        elif nama == "":
                            print("Nama makanan tidak boleh kosong!")
                            press_enter()
                            return
                        else:
                            print("Penambahan menu dibatalkan.")
                            press_enter()
                            return
                else:
                    print(f"Nama makanan tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        nama = input("Nama makanan: ").strip()
                    else:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return
                    
            kalori = input("Kalori: ").strip()
            for kesempatan in range(3):
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
                if harga == "":
                    print(f"Harga tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                elif harga.isdigit():
                    if harga == "0":
                        print(f"Harga harus lebih dari 0! (sisa kesempatan: {2 - kesempatan})")
                    elif harga < "0":
                        print(f"Harga harus lebih dari 0! (sisa kesempatan: {2 - kesempatan})")
                    else:
                        harga = int(harga)
                        break
                elif not harga.isdigit():
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
                    if stok <= "0":
                        print(f"Stok tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                    elif stok < "0":
                        print(f"Stok tidak boleh negatif! (sisa kesempatan: {2 - kesempatan})")
                    else:
                        stok = int(stok)
                        break
                elif not stok.isdigit():
                    print(f"Stok harus berupa angka! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Penambahan menu dibatalkan.")
                    press_enter()
                    return

            if kalori() and harga() and stok():
                tambah_makanan(nama, user["toko"], int(kalori), int(harga), int(stok))
            press_enter()

        elif pilih == "2":
            print(toko_df[["nama", "kalori", "harga", "stok"]].assign(no=range(1, len(toko_df) + 1))[["no", "nama", "kalori", "harga", "stok"]].to_string(index=False))
            idx = input("Index makanan: ").strip()
            if idx.isdigit():
                idx = int(idx) - 1
                if idx < 0 or idx >= len(toko_df):
                    print("Index tidak ditemukan.")
                    press_enter()
                    continue  
            else:
                print("Index tidak valid, masukkan angka.")
                press_enter()
                continue
            
            baris_asli = toko_df.loc[idx, "__idx"]
            
            nama_lama = df.at[baris_asli, "nama"]
            nama = input("Nama baru: ").strip()
            for kesempatan in range(3):
                if nama:
                    nama_lower_list = df["nama"].str.lower().values
                    if nama.lower() in nama_lower_list and nama.lower() != nama_lama.lower():
                        print(f"Nama makanan '{nama}' sudah ada di toko Anda! (sisa kesempatan: {2 - kesempatan})")
                        if kesempatan < 2:
                            nama = input("Nama baru: ").strip()
                        else:
                            print("Update dibatalkan.")
                            press_enter()
                            continue
                    else:
                        break
                else:
                    print(f"Nama tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        nama = input("Nama baru: ").strip()
                    else:
                        print("Update dibatalkan.")
                        press_enter()
                        continue
            
            kalori = input("Kalori baru: ").strip()
            for kesempatan in range(3):
                if kalori and kalori.isdigit():
                    break
                else:
                    print(f"Kalori harus angka positif! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        kalori = input("Kalori baru: ").strip()
                    else:
                        print("Update dibatalkan.")
                        press_enter()
                        continue
          
            harga = input("Harga baru: ").strip()
            for kesempatan in range(3):
                if harga and harga.isdigit():
                    break
                else:
                    print(f"Harga harus angka positif! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        harga = input("Harga baru: ").strip()
                    else:
                        print("Update dibatalkan.")
                        press_enter()
                        continue
            
            stok = input("Stok baru: ").strip()
            for kesempatan in range(3):
                if stok and stok.isdigit():
                    break
                else:
                    print(f"Stok harus angka positif! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        stok = input("Stok baru: ").strip()
                    else:
                        print("Update dibatalkan.")
                        press_enter()
                        continue
            
            df.at[baris_asli, "nama"] = nama
            df.at[baris_asli, "kalori"] = int(kalori)
            df.at[baris_asli, "harga"] = int(harga)
            df.at[baris_asli, "stok"] = int(stok)
            
            save_makanan(df)
            print("Makanan berhasil di-update.")
            press_enter()

        elif pilih == "3":
            idx = input("Index makanan: ").strip()

            if idx.isdigit():
                idx = int(idx) - 1

                if idx < 0 or idx >= len(toko_df):
                    print("Index tidak ditemukan.")
                    press_enter()
                    return

                baris_asli = toko_df.loc[idx, "__idx"]
                df = df.drop(baris_asli).reset_index(drop=True)

                save_makanan(df)
                press_enter()
            else:
                print("Index tidak valid, masukkan angka.")
                press_enter()
                return

        elif pilih == "0":
            break

def kelola_stok(user):
    clear_screen()
    df = load_makanan().reset_index(drop=True)
    toko_df = df[df["restoran"] == user["toko"]].copy()
    toko_df["__idx"] = toko_df.index
    toko_df = toko_df.reset_index(drop=True)

    if toko_df.empty:
        print("Belum ada makanan di toko Anda.")
        press_enter()
        return

    print(toko_df[["nama","stok"]].assign(no=range(1, len(toko_df) + 1))[["no","nama","stok"]].to_string(index=False))

    idx = input("Index makanan: ").strip()
    if not idx.isdigit():
        print("Index tidak valid, masukkan angka.")
        press_enter()
        return

    idx = int(idx) - 1
    if idx < 0 or idx >= len(toko_df):
        print("Index tidak ditemukan.")
        press_enter()
        return

    baris_asli = toko_df.loc[idx, "__idx"]

    stok = input("Stok baru: ").strip()
    if not stok.isdigit():
        print("Stok harus berupa angka.")
        press_enter()
        return

    stok = int(stok)
    if stok < 0:
        print("Stok tidak boleh negatif.")
        press_enter()
        return

    df.at[baris_asli, "stok"] = stok
    save_makanan(df)

    print("Stok berhasil diperbarui.")
    press_enter()

def laporan_penjualan(user):
    clear_screen()

    df = load_makanan()
    toko_df = df[df["restoran"] == user["toko"]].copy()

    if toko_df.empty:
        print("Belum ada menu di toko Anda.")
        press_enter()
        return

    sales_qty = {}  
    if PENJUALAN_CSV.exists():
        with open(PENJUALAN_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "nama_makanan" not in reader.fieldnames or "restoran" not in reader.fieldnames or "qty" not in reader.fieldnames:
                print("Format data penjualan tidak valid.")
                press_enter()
                return
            for row in reader:
                if row["restoran"] == user["toko"]:
                    menu_name = row["nama_makanan"]
                    qty = int(row["qty"])
                    sales_qty[menu_name] = sales_qty.get(menu_name, 0) + qty  
    print("Laporan Penjualan Toko Anda:")
    print("-" * 50)
    total_penjualan = 0
    for _, row in toko_df.iterrows():
        menu_name = row["nama"]  
        harga = int(row["harga"]) 
        qty_terjual = sales_qty.get(menu_name, 0)  
        pendapatan = qty_terjual * harga
        total_penjualan += pendapatan
        print(f"{menu_name}: {qty_terjual} terjual, Pendapatan: Rp{pendapatan}")

    print("-" * 50)
    print(f"Total Pendapatan: Rp{total_penjualan}")
    press_enter()

def menu_mitra(user):
    while True:
        clear_screen()
        print(f"=== MITRA: {user['nama']} ({user['toko']}) ===")
        print("1. Profil Toko")
        print("2. Kelola Menu Makanan")
        print("3. Kelola Stok")
        print("4. Laporan Penjualan")
        print("0. Logout")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            profil_toko(user)
        elif pilih == "2":
            kelola_menu(user)
        elif pilih == "3":
            kelola_stok(user)
        elif pilih == "4":
            laporan_penjualan(user)
        elif pilih == "0":
            break


