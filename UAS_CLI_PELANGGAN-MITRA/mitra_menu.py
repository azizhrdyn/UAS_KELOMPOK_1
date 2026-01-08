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

        for kesempatan in range(3):
            lokasi = input(f"Lokasi [{profil['lokasi']}]: ").strip()
            if not lokasi:
                print(f"Lokasi tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
            elif all(c.isalnum() or c in " .,/" for c in lokasi):
                break
            else:
                print(f"Lokasi hanya boleh berisi huruf, angka, spasi, titik, dan koma. (sisa kesempatan: {2 - kesempatan})")
            
            if kesempatan == 2:
                print("Edit profil dibatalkan.")
                press_enter()
                return
        
        for kesempatan in range(3):
            jam = input(f"Jam Operasional [{profil['jam_operasional']}]: ").strip() or profil["jam_operasional"]
        
            pola = r"^(?:[01]\d|2[0-3])[:.][0-5]\d\s*[-–]\s*(?:[01]\d|2[0-3])[:.][0-5]\d$"
        
            if re.match(pola, jam):
                break
            else:
                print(f"Format jam tidak valid! Contoh: 08.00 - 17.00 atau 08:00-17:00 "
                      f"(sisa kesempatan: {2 - kesempatan})")
        
        for kesempatan in range(3):
            desk = input(f"Deskripsi [{profil['deskripsi']}]: ") or profil["deskripsi"]
            if not desk:
                print(f"Input tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
            elif all(c.isalnum() or c in " .,/" for c in desk):
                break
            else:
                print(f"Deskripsi toko hanya boleh berisi huruf, angka, spasi, titik, dan koma. (sisa kesempatan: {2 - kesempatan})")

        edit_profil_toko(user["username"], {
            "lokasi": lokasi,
            "jam_operasional": jam,
            "deskripsi": desk
        })

        print("\nProfil toko berhasil diperbarui.")
        press_enter()
    elif sub == "2":
        return
    elif not sub:
        print("Input tidak boleh kosong.")
        press_enter()
    else:
        print("Pilihan tidak valid.")
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
            clear_screen()
            print("=== TAMBAH MAKANAN BARU ===")
                
            for kesempatan in range(3):
                nama = input("Nama Makanan: ").strip()
                if nama.lower() in toko_df["nama"].str.lower().values:
                        print(f"Nama makanan '{nama}' sudah ada di toko Anda! (sisa kesempatan: {2 - kesempatan})")
                elif nama == "":
                    print(f"Nama makanan tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                else:
                    break
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

            tambah_makanan(nama, user["toko"], kalori, harga, stok)
            print("Makanan baru berhasil ditambahkan.")
            press_enter()

        elif pilih == "2":
            df = load_makanan().reset_index(drop=True)
            toko_df = df[df["restoran"] == user["toko"]]
        
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
                
            nama = input("Nama baru: ").strip()
            for kesempatan in range(3):
                if nama:
                    if nama in toko_df["nama"].values and nama != toko_df.at[idx, "nama"]:
                        print(f"Nama makanan '{nama}' sudah ada di toko Anda! (sisa kesempatan: {2 - kesempatan})")
                        if kesempatan < 2:
                            nama = input("Nama makanan: ").strip()
                        else:
                            print("Penambahan menu dibatalkan.")
                            press_enter()
                            return
                    break
                else:
                    print(f"Nama makanan tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                    if kesempatan < 2:
                        nama = input("Nama makanan: ").strip()
                    else:
                        print("Penambahan menu dibatalkan.")
                        press_enter()
                        return
                    
            kalori = input("Kalori baru: ").strip()
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
                        
            harga = input("Harga baru: ").strip()
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
                    
            stok = input("Stok baru: ").strip()
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

            baris_asli = toko_df.index[idx]
        
            update_makanan(
                baris_asli,
                nama if nama else None,
                int(kalori) if kalori.isdigit() else None,
                int(harga) if harga.isdigit() else None,
                int(stok) if stok.isdigit() else None
            )
        
            print("Menu berhasil diperbarui.")
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
            

