import os
import sys

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def press_enter(msg="\nTekan ENTER untuk kembali..."):
    input(msg)

def safe_int(s, default=0):
    try:
        return int(s)
    except:
        return default

def exit_program():
    print("Keluar...")
    sys.exit(0)

