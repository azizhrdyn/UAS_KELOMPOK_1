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
