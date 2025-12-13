from database_makanan import load_makanan
import pandas as pd

def rekomendasi_kalori(max_kalori=300):
    df = load_makanan()
    return df[df['kalori'] <= max_kalori]

def rekomendasi_harga(max_harga=10000):
    df = load_makanan()
    return df[df['harga'] <= max_harga]

def rekomendasi_terbaik(jumlah=3):
    df = load_makanan().copy()
    if df.empty:
        return df
    df['skor'] = df['harga'].astype(float)*0.7 + df['kalori'].astype(float)*0.3
    df_sorted = df.sort_values('skor').head(jumlah)
    return df_sorted.drop(columns=["skor"])

def print_hasil(df, judul="Hasil"):
    print(f"\n=== {judul} ===")
    if df is None or df.empty:
        print("Tidak ada rekomendasi tersedia.")
        return
    print(df[["nama","restoran","kalori","harga"]].to_string(index=False))

def menu_rekomendasi():
    while True:
        print("\n=== MENU REKOMENDASI MAKANAN ===")
        print("1. Rekomendasi Kalori Rendah")
        print("2. Rekomendasi Harga Murah")
        print("3. Rekomendasi Terbaik")
        print("0. Kembali")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            batas = input("Batas kalori (default 300): ").strip()
            batas = int(batas) if batas else 300
            df = rekomendasi_kalori(batas)
            print_hasil(df, f"Kalori ≤ {batas}")
            input("\nENTER...")
        elif pilih == "2":
            batas = input("Batas harga (default 10000): ").strip()
            batas = int(batas) if batas else 10000
            df = rekomendasi_harga(batas)
            print_hasil(df, f"Harga ≤ Rp{batas}")
            input("\nENTER...")
        elif pilih == "3":
            jumlah = input("Top berapa? (default 3): ").strip()
            jumlah = int(jumlah) if jumlah else 3
            df = rekomendasi_terbaik(jumlah)
            print_hasil(df, f"Top {jumlah} Terbaik")
            input("\nENTER...")
        elif pilih == "0":
            break
        else:
            print("Pilihan tidak valid!")
            
