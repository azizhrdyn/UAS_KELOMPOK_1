import time

EWALLETS = ["Dana", "ShopeePay", "OVO", "GoPay", "PayPal", "LinkAja"]

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
    
