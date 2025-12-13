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
