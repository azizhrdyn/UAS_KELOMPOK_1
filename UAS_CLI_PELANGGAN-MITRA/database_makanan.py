import pandas as pd
from pathlib import Path

CSV_PATH = Path("makanan.csv")

DEFAULT_COLUMNS = ["nama", "restoran", "kalori", "harga"]

def ensure_csv_exists():
    if not CSV_PATH.exists():
        # buat file contoh kosong
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(CSV_PATH, index=False)
        
def load_makanan():
    ensure_csv_exists()
    df = pd.read_csv(CSV_PATH)
    # pastikan kolom ada
    for c in DEFAULT_COLUMNS:
        if c not in df.columns:
            df[c] = ""
    return df
