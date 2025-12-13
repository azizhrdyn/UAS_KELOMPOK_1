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
