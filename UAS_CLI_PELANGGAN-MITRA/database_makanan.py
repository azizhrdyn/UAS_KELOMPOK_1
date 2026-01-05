import pandas as pd
from pathlib import Path
import numpy as np

CSV_PATH = Path("makanan.csv")

DEFAULT_COLUMNS = ["nama", "restoran", "kalori", "harga", "stok"]

def ensure_csv_exists():
    if not CSV_PATH.exists():
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(CSV_PATH, index=False)

def load_makanan():
    ensure_csv_exists()
    df = pd.read_csv(CSV_PATH)
    for c in DEFAULT_COLUMNS:
        if c not in df.columns:
            df[c] = 0
    return df

def save_makanan(df):
    df.to_csv(CSV_PATH, index=False)

def tambah_makanan(nama, restoran, kalori, harga, stok):
    df = load_makanan()
    df.loc[len(df)] = [nama, restoran, kalori, harga, stok]
    save_makanan(df)

def update_makanan(idx, nama=None, kalori=None, harga=None, stok=None):
    df = load_makanan()
    if idx not in df.index:
        return
    else:
        idx = int(idx)
    if nama is not None:
        df.at[idx, "nama"] = nama
    if kalori is not None:
        df.at[idx, "kalori"] = kalori
    if harga is not None:
        df.at[idx, "harga"] = harga
    if stok is not None:
        df.at[idx, "stok"] = stok
    save_makanan(df)

def hapus_makanan(df, baris_asli):
    df = df.drop(baris_asli).reset_index(drop=True)
    save_makanan(df)
    return df

def linear_search_makanan(df, keyword):
    keyword = keyword.lower()
    nama_array = np.array(df["nama"].str.lower())
    hasil_index = []

    for i in range(len(nama_array)):
        kata_kata = nama_array[i].split()
        for kata in kata_kata:
            if kata.startswith(keyword):
                hasil_index.append(i)
                break
                
    return df.iloc[hasil_index]
