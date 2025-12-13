from database_makanan import load_makanan
import pandas as pd

def rekomendasi_kalori(max_kalori=300):
    df = load_makanan()
    return df[df['kalori'] <= max_kalori]

def rekomendasi_harga(max_harga=10000):
    df = load_makanan()
    return df[df['harga'] <= max_harga]
