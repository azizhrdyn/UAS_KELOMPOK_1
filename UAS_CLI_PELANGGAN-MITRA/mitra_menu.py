from database_makanan import load_makanan, save_makanan, tambah_makanan, update_makanan, hapus_makanan
from utils import press_enter, clear_screen
import csv
from pathlib import Path
from auth import get_profil_toko, edit_profil_toko

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
        jam = input(f"Jam Operasional [{profil['jam_operasional']}]: ") or profil["jam_operasional"]
        desk = input(f"Deskripsi [{profil['deskripsi']}]: ") or profil["deskripsi"]

        edit_profil_toko(user["username"], {
            "lokasi": lokasi,
            "jam_operasional": jam,
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
                    if nama in toko_df["nama"].values:
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
            idx = input("Index makanan: ").strip()
            if idx.isdigit():
                idx = int(idx) - 1
                if idx < 0 or idx >= len(df):
                    print("Index tidak ditemukan.")
                    press_enter()
                    return
            else:
                print("Index tidak valid, masukkan angka.")
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

            update_makanan(
                idx,
                nama if nama else None,
                int(kalori) if kalori.isdigit() else None,
                int(harga) if harga.isdigit() else None,
                int(stok) if stok.isdigit() else None
            )
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
