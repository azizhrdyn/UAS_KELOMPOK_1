from utils import clear_screen, press_enter, exit_program
from auth import login, register_user, valid_username, valid_password, valid_name, input_nama, input_username, input_password, input_role, input_toko
from pelanggan_menu import menu_pelanggan
from mitra_menu import menu_mitra
from admin_menu import menu_admin

def main():
    while True:
        clear_screen()
        print("=== FLAVOR OF ONE DAY ===")
        print("1. Login")
        print("2. Register")
        print("0. Keluar")

        p = input("Pilih: ").strip()

        if p == "1":
            clear_screen()
            user = login()
            if user:
                if user["role"] == "pelanggan":
                    menu_pelanggan(user)
                elif user["role"] == "mitra":
                    menu_mitra(user)
                elif user["role"] == "admin":
                    menu_admin(user)

        elif p == "2":
            clear_screen()
            print("=== REGISTER ===")
            username = input_username()
            if not username:
                continue
            password = input_password()
            if not password:
                continue
            nama = input_nama()
            if not nama:
                continue
            role = input_role()
            if not role:
                continue
            toko = ""
            if role == "mitra":
                toko = input_toko()
                if not toko:
                    continue
            if valid_username(username) and valid_password(password) and valid_name(nama):
                register_user(username, password, role, nama, toko)

            success = register_user(username, password, role, nama)
            if success:
                print("Registrasi berhasil. Silakan login.")
                break
            press_enter()

        elif p == "0":
            exit_program()

if __name__ == "__main__":
    main()

