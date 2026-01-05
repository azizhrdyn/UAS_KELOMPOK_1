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
                    # Cek sudah ada apa belum di toko walaupun huruf besar kecilnya beda tetap di hitung sama
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
                        
            harga = input("Harga: ").strip()
            for kesempatan in range(3):
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

            stok = input("Stok: ").strip()
            for kesempatan in range(3):
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
                tambah_makanan(nama, user["toko"], int(kalori), int(harga), int(stok))
            press_enter()

        elif pilih == "2":
            # Tampilkan daftar toko_df untuk pilih index
            print(toko_df[["nama", "kalori", "harga", "stok"]].assign(no=range(1, len(toko_df) + 1))[["no", "nama", "kalori", "harga", "stok"]].to_string(index=False))
            #assign adalah untuk menambahkan kolom no sebagai index yang ditampilkan ke user
            #to_string untuk menampilkan dataframe sebagai string tanpa index asli

            if idx.isdigit():
                idx = int(idx) - 1
                if idx < 0 or idx >= len(toko_df):
                    print("Index tidak ditemukan.")
                    press_enter()
                    continue  # Kembali ke menu, bukan return
                #idx adalah index yang dipilih user dikurangi 1 untuk menyesuaikan dengan index 0-based
            else:
                print("Index tidak valid, masukkan angka.")
                press_enter()
                continue
            
            # Dapatkan baris asli di df utama
            baris_asli = toko_df.loc[idx, "__idx"]
            
            # Input nama baru dengan cek duplikat (case-insensitive, exclude yang sedang diupdate)
            nama_lama = df.at[baris_asli, "nama"]
            nama = input("Nama baru: ").strip()
            for kesempatan in range(3):
                if nama:
                    # Cek duplikat di df utuh, case-insensitive, tapi abaikan nama lama
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
            
            # Input kalori baru
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
            
            # Input harga baru
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
            
            # Input stok baru
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
            
            # Update df utama langsung
            df.at[baris_asli, "nama"] = nama
            df.at[baris_asli, "kalori"] = int(kalori)
            df.at[baris_asli, "harga"] = int(harga)
            df.at[baris_asli, "stok"] = int(stok)
            
            # Simpan df utama
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

    if not PENJUALAN_CSV.exists():
        print("Belum ada penjualan.")
        press_enter()
        return
    
    with open(PENJUALAN_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "restoran" not in reader.fieldnames:
            print("Format data penjualan tidak valid.")
            press_enter()
            return

        data = [r for r in reader if r["restoran"] == user["toko"]]

    if not data:
        print("Belum ada penjualan.")
        press_enter()
        return

    total = 0
    for r in data:
        print(f"{r['nama_makanan']} x{r['qty']} = Rp{r['subtotal']}")
        total += int(r["subtotal"])

    print("\nTotal Penjualan: Rp", total)
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
