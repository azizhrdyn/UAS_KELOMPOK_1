import time
from database_makanan import load_makanan
from utils import press_enter

EWALLETS = ["Dana", "ShopeePay", "OVO", "GoPay", "PayPal", "LinkAja"]

def order_makanan():
    df = load_makanan()
    if df.empty:
        print("Belum ada makanan.")
        press_enter()
        return

    print(df[["nama","restoran","kalori","harga"]].to_string(index=True))
    pilih_idx = input("Masukkan index makanan (pisah koma): ").strip()
    if not pilih_idx:
        return

    try:
        indices = [int(x.strip()) for x in pilih_idx.split(",")]
    except:
        print("Input index tidak valid.")
        press_enter()
        return

    order_lines = []
    total = 0
    for idx in indices:
        if idx in df.index:
            while True:
                qty = input(f"Jumlah '{df.at[idx,'nama']}' : ").strip()
                if qty.isdigit() and int(qty) > 0:
                    qty = int(qty)
                    break
            harga = int(df.at[idx,'harga'])
            subtotal = harga * qty
            order_lines.append((df.at[idx,'nama'], df.at[idx,'restoran'], qty, harga, subtotal))
            total += subtotal

    if not order_lines:
        print("Tidak ada item valid.")
        press_enter()
        return

    print("\n=== Ringkasan Order ===")
    for o in order_lines:
        print(f"{o[0]} ({o[1]}) x{o[2]} - Rp{o[4]}")
    print("Total: Rp", total)

    konfirm = input("Lanjut ke pembayaran? (y/n): ").lower()
    if konfirm == "y":
        simulasi_pembayaran(total)

    press_enter()

def pilih_metode():
    print("\nPilih metode pembayaran (simulasi):")
    for i, m in enumerate(EWALLETS, start=1):
        print(f"{i}. {m}")
    pilih = input("Pilih metode (nomor): ").strip()
    try:
        idx = int(pilih) - 1
        if 0 <= idx < len(EWALLETS):
            return EWALLETS[idx]
    except:
        pass
    return None

def simulasi_pembayaran(total):
    metode = pilih_metode()
    if not metode:
        print("Metode tidak valid.")
        return False
    print(f"\nKamu memilih {metode}. Jumlah: Rp{total}")
    ident = input("Masukkan nomor/ID e-wallet (simulasi): ").strip()
    if not ident:
        print("ID tidak valid.")
        return False
    print("Memproses pembayaran...", end="", flush=True)
    time.sleep(1.2)
    print(".", end="", flush=True)
    time.sleep(0.8)
    print(" Sukses!")
    print(f"Pembayaran sebesar Rp{total} berhasil melalui {metode} (ID: {ident}).")
    return True
