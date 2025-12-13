import pandas as pd
from database_makanan import load_makanan, save_makanan, reload_from_csv
from utils import safe_int

def lihat_data():
    df = load_makanan()
    if df.empty:
        print("\nBelum ada data makanan.")
    else:
        print(df[["nama","restoran","kalori","harga"]].to_string(index=True))
    input("\nENTER untuk kembali...")

def tambah_data():
    print("\n=== Tambah Data Makanan (Mitra) ===")
    nama = input("Nama makanan   : ").strip()
    restoran = input("Nama restoran  : ").strip()
    kalori = safe_int(input("Kalori (angka) : "), 0)
    harga = safe_int(input("Harga (angka)  : "), 0)
    
df = load_makanan()
    new = {"nama": nama, "restoran": restoran, "kalori": kalori, "harga": harga}
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv("makanan.csv", index=False)
    print("Data berhasil ditambahkan.")
    input("\nENTER...")



def hapus_data():
    df = load_makanan()
    print(df[["nama","restoran","kalori","harga"]].to_string(index=True))
    idx = input("Masukkan index baris yang akan dihapus (atau kosong): ").strip()
    if idx == "":
        return
    try:
        idx = int(idx)
        if idx in df.index:
            row = df.loc[idx].to_dict()
            print("Kosongkan input untuk mempertahankan nilai lama.")
            nama = input(f"Nama ({row['nama']}): ").strip() or row['nama']
            restoran = input(f"Restoran ({row['restoran']}): ").strip() or row['restoran']
            kalori = input(f"Kalori ({row['kalori']}): ").strip()
            harga = input(f"Harga ({row['harga']}): ").strip()
            kalori = safe_int(kalori, int(row['kalori']))
            harga = safe_int(harga, int(row['harga']))
            df.at[idx, 'nama'] = nama
            df.at[idx, 'restoran'] = restoran
            df.at[idx, 'kalori'] = kalori
            df.at[idx, 'harga'] = harga
            save_makanan(df)
            print("Data berhasil diupdate.")
        else:
            print("Index tidak ditemukan.")
    except Exception as e:
        print("Terjadi error:", e)
    input("\nENTER...")

def reload_csv():
    print("Reloading dari file CSV...")
    df = reload_from_csv()
    print("Reload selesai. Jumlah baris:", len(df))
    input("\nENTER...")

