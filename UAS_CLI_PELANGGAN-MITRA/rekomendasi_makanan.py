from database_makanan import load_makanan
from utils import press_enter, clear_screen
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
    print(df[["nama","restoran","kalori","harga"]].assign(no=range(1, len(df) + 1))[["no","nama","restoran","kalori","harga"]].to_string(index=False))

def menu_rekomendasi():
    while True:
        print("=== MENU REKOMENDASI MAKANAN ===")
        print("1. Rekomendasi Kalori Rendah")
        print("2. Rekomendasi Harga Murah")
        print("3. Rekomendasi Terbaik")
        print("0. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            clear_screen()
            while True:
                batas = input("Batas kalori (default 300): ").strip()
                if batas.isdigit() or batas == "":
                    break
                else:
                    print("Batas kalori harus berupa angka dan tidak boleh kosong!")
            df = rekomendasi_kalori(int(batas)) if batas else rekomendasi_kalori()
            print_hasil(df, f"Kalori ≤ {batas}")
            press_enter()
            break
            
        elif pilih == "2":
            clear_screen()
            while True:
                batas = input("Batas harga (default 10000): ").strip()
                if batas.isdigit() or batas == "":
                    break
                else:
                    print("Batas harga harus berupa angka dan tidak boleh kosong!")
            df = rekomendasi_harga(int(batas)) if batas else rekomendasi_harga()
            print_hasil(df, f"Harga ≤ Rp{batas}")
            press_enter()
            break
            
        elif pilih == "3":
            clear_screen()
            while True:
                jumlah = input("Berapa banyak rekomendasi terbaik yang diinginkan? (default 3): ").strip()
                if jumlah.isdigit() or jumlah == "":
                    break
                else:
                    print("Jumlah harus berupa angka dan tidak boleh kosong!")
            df = rekomendasi_terbaik(int(jumlah)) if jumlah else rekomendasi_terbaik()
            print_hasil(df, f"Top {jumlah} Terbaik")
            press_enter()
            break
            
        elif pilih == "0":
            break
        
        else:
            print("Pilihan tidak valid!")
            press_enter()
            break
