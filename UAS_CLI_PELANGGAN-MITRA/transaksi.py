from database_makanan import load_makanan, save_makanan
from utils import press_enter, clear_screen
import sys
import time
import csv
from pathlib import Path

PENJUALAN_CSV = Path("penjualan.csv")
USER_CSV = Path("user.csv")

EWALLETS = ["Dana", "ShopeePay", "OVO", "GoPay", "PayPal", "LinkAja"]

def get_alamat_tersimpan(username):
    if not USER_CSV.exists():
        return None

    with open(USER_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                alamat = row.get("alamat", "").strip()
                return alamat if alamat else None
    return None

def ensure_penjualan_csv():
    if not PENJUALAN_CSV.exists():
        with open(PENJUALAN_CSV, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nama_makanan", "restoran", "qty", "harga", "subtotal"])

def input_alamat_pengiriman():
    for kesempatan in range(3):
        alamat = input("Masukkan alamat pengiriman: ").strip()
        if alamat:
            return alamat
        else:
            print(f"Alamat tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")

    print("Gagal input alamat.")
    press_enter()
    return None

def pilih_alamat(alamat_tersimpan):
    print("\nPilih alamat pengiriman:")
    print("1. Gunakan alamat tersimpan")
    print("2. Input alamat baru")

    for kesempatan in range(3):
        pilih = input("Pilih opsi (1/2): ").strip()

        if pilih == "1":
            if alamat_tersimpan:
                print("Menggunakan alamat tersimpan.")
                return alamat_tersimpan
            else:
                print("Belum ada alamat tersimpan.")
                press_enter()
                return None

        elif pilih == "2":
            return input_alamat_pengiriman()

        else:
            print(f"Pilihan tidak valid! (sisa kesempatan: {2 - kesempatan})")

    print("Gagal memilih alamat.")
    press_enter()
    return None

def order_makanan(user):
    df = load_makanan()
    if df.empty:
        print("Belum ada makanan.")
        press_enter()
        return

    print(df[["nama","restoran","kalori","harga","stok"]].assign(no=range(1, len(df) + 1))[["no","nama","restoran","kalori","harga","stok"]].to_string(index=False))
    pilih_idx = input("Masukkan index makanan (pisah koma): ").strip()
    if not pilih_idx.replace(",", "").isdigit():
        print("Input index tidak valid.")
        press_enter()
        return
    indices = [int(x) - 1 for x in pilih_idx.split(",")]
    
    if any(i < 0 or i >= len(df) for i in indices):
        print("Index di luar jangkauan.")
        press_enter()
        return

    order_lines = []
    total = 0
    clear_screen()

    for idx in indices:
        if idx in df.index:
            stok = int(df.at[idx, "stok"])
            if stok <= 0:
                continue

            qty = None
            for kesempatan in range(3):
                qty_input = input(f"Jumlah '{df.at[idx,'nama']}' : ").strip()
            
                if not qty_input:
                    print(f"Jumlah tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
                elif qty_input.isdigit() and 0 < int(qty_input) <= stok:
                    qty = int(qty_input)
                    break
                else:
                    print(f"Jumlah harus berupa angka antara 1 dan {stok} berdasarkan jumlah stok yang tersedia. (sisa kesempatan: {2 - kesempatan}).")
            
            if qty is None:
                print("Gagal menambahkan makanan ke pesanan.")
                continue
                
            harga = int(df.at[idx,'harga'])
            subtotal = harga * qty

            order_lines.append((idx, df.at[idx,'nama'], df.at[idx,'restoran'], qty, harga, subtotal))
            total += subtotal

    if not order_lines:
        print("Tidak ada item valid.")
        press_enter()
        return
        
    username_login = user["username"]
    alamat_tersimpan = get_alamat_tersimpan(username_login)
    
    alamat = pilih_alamat(alamat_tersimpan)
    if alamat is None:
        return

    clear_screen()
    print("=== Ringkasan Order ===")
    for o in order_lines:
        print(f"{o[1]} ({o[2]}) x{o[3]} - Rp{o[5]}")
    print("Total: Rp", total)
    print(f"Alamat Pengiriman: {alamat}")
    
    for kesempatan in range(3):
        konfirm = input("Lanjut ke pembayaran? (y/n): ").strip().lower()
    
        if not konfirm:
            print(f"Input tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
        elif konfirm == "y":
            break
        elif konfirm == "n":
            print("Order dibatalkan.")
            press_enter()
            return
        else:
            print(f"Pilih 'y' atau 'n'! (sisa kesempatan: {2 - kesempatan})")
    
        if kesempatan == 2:
            print("Order dibatalkan.")
            press_enter()
            return

    if not simulasi_pembayaran(total):
        return

    ensure_penjualan_csv()

    with open(PENJUALAN_CSV, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for o in order_lines:
            writer.writerow([o[1], o[2], o[3], o[4], o[5]])
            df.at[o[0], "stok"] -= o[3]

    save_makanan(df)
    press_enter()

def pilih_metode():
    print("\nPilih metode pembayaran (simulasi):")
    for i, m in enumerate(EWALLETS, start=1):
        print(f"{i}. {m}")
    print("0. Batal")
    while True:
        pilih = input("Pilih metode (nomor): ").strip()
        if pilih == "0":
            print("Pembayaran dibatalkan.")
            press_enter()
            return None

        if not pilih.isdigit():
            print("Pilihan tidak valid. Masukkan nomor yang sesuai atau 0 untuk batal.")
            continue

        idx = int(pilih) - 1
        if 0 <= idx < len(EWALLETS):
            return EWALLETS[idx]
        else:
            print(f"Pilihan di luar jangkauan. Masukkan angka antara 1 dan {len(EWALLETS)} atau 0 untuk batal.")

def simulasi_pembayaran(total):
    metode = pilih_metode()
    while True:
        if metode is None:
            return False
        print(f"Metode pembayaran terpilih: {metode}")
        for kesempatan in range(3):
            konfirm = input("Lanjutkan pembayaran? (y/n): ").strip().lower()
            if not konfirm:
                print(f"Input tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
            elif konfirm == "y":
                break
            elif konfirm == "n":
                press_enter()
                return False
            else:
                print(f"Pilih 'y' atau 'n'! (sisa kesempatan: {2 - kesempatan})")
            if kesempatan == 2:
                print("Pembayaran dibatalkan.")
                press_enter()
                return False
                
        for kesempatan in range(3):
            ident = input(f"Masukkan nomor/ID e-wallet {metode} (simulasi): ").strip()
            if ident.isdigit() and len(ident) >= 10:
                clear_screen()
                print("Memproses pembayaran", end="", flush=True)
                for _ in range(3):
                    time.sleep(1)
                    print(".", end="", flush=True)
                print("\nPembayaran berhasil. Terima kasih atas pesanan Anda!")
                return True
            elif not ident:
                print(f"ID e-wallet tidak boleh kosong! (sisa kesempatan: {2 - kesempatan})")
            else:
                print(f"ID e-wallet harus berupa angka dan minimal 10 digit! (sisa kesempatan: {2 - kesempatan})")
                if kesempatan == 2:
                    print("Pembayaran dibatalkan.")
                    press_enter()
                    return False
