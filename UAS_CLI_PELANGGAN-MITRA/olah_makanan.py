def bubble_sort_list_of_dicts(lst, key):
    arr = lst.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def search_by_name(df, keyword):
    kw = keyword.lower()
    return df[df['nama'].str.lower().str.contains(kw, na=False)]
    
def menu_olah_makanan():
    df = load_makanan()
    while True:
        print("\n=== Olah Data (Sorting & Searching) ===")
        print("1. Sorting berdasarkan harga (ascending)")
        print("2. Sorting berdasarkan kalori (ascending)")
        print("3. Cari makanan (nama)")
        print("4. Tampilkan array harga (NumPy) + contoh searching")
        print("0. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            df_sorted = df.sort_values("harga")
            print(df_sorted[["nama","restoran","harga"]].to_string(index=False))
            input("\nENTER untuk kembali...")
        elif pilih == "2":
            df_sorted = df.sort_values("kalori")
            print(df_sorted[["nama","restoran","kalori"]].to_string(index=False))
            input("\nENTER untuk kembali...")
        elif pilih == "3":
            keyword = input("Cari nama: ").strip()
            hasil = search_by_name(df, keyword)
            if hasil.empty:
                print("Tidak ditemukan.")
            else:
                print(hasil[["nama","restoran","kalori","harga"]].to_string(index=False))
            input("\nENTER untuk kembali...")
            
