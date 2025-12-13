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
