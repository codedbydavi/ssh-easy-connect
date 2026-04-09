import os
import sys
import base64
import getpass
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from modules.constants import CONFIG_FILE

_cipher = None

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def get_cipher():
    global _cipher
    return _cipher

def set_cipher(cipher):
    global _cipher
    _cipher = cipher

def init_crypto(save_data_callback):
    global _cipher
    if not CONFIG_FILE.exists():
        print("--- Initial Setup ---")
        while True:
            pwd = getpass.getpass("Set a master password: ")
            if len(pwd) < 8:
                print("Password must be at least 8 characters long.")
                continue
            confirm_pwd = getpass.getpass("Confirm master password: ")
            if pwd != confirm_pwd:
                print("Passwords do not match. Please try again.")
                continue
            print("The master password has been set.")
            break
        salt = os.urandom(16)
        _cipher = Fernet(derive_key(pwd, salt))
        save_data_callback({
            "salt": base64.b64encode(salt).decode(),
            "servers": [],
            "snippets": [{"name": "Disk Usage", "command": "df -h"}]
        })
        return
    
    with open(CONFIG_FILE, "r") as f: data = json.load(f)
        
    if isinstance(data, list):
        print("--- Security Update ---")
        while True:
            pwd = getpass.getpass("Set a master password: ")
            if len(pwd) < 8:
                print("Password must be at least 8 characters long.")
                continue
            confirm_pwd = getpass.getpass("Confirm master password: ")
            if pwd != confirm_pwd:
                print("Passwords do not match. Please try again.")
                continue
            print("The master password has been set.")
            break
        salt = os.urandom(16)
        _cipher = Fernet(derive_key(pwd, salt))
        new_data = {
            "salt": base64.b64encode(salt).decode(),
            "servers": [],
            "snippets": [{"name": "Disk Usage", "command": "df -h"}]
        }
        for s in data:
            enc_pw = _cipher.encrypt(s["password"].encode()).decode() if s.get("password") else ""
            new_data["servers"].append({
                "name": s["name"],
                "user": s["user"],
                "host": s["host"],
                "port": s.get("port", 22),
                "password": enc_pw,
                "group": s["group"] if s.get("group") else "Ungrouped"
            })
        save_data_callback(new_data)
    else:
        salt = base64.b64decode(data["salt"])
        pwd = getpass.getpass(" 🔑 Master password: ")
        _cipher = Fernet(derive_key(pwd, salt))
        try:
            for s in data.get("servers", []):
                if s.get("password"):
                    _cipher.decrypt(s["password"].encode())
                    break
        except:
            print(" ❌ Incorrect master password. Exiting.")
            sys.exit(1)
