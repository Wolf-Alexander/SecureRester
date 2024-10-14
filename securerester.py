# This project was initially inspired by the concept of securesyncer
# (https://github.com/AshrafAkon/securesyncer), but has been significantly
# modified to use a different cryptographic approach and data storage format.
import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def create_key():
    try:
        with open("key.key", "rb") as key_file:
            pass  # File exists, no need to create
    except FileNotFoundError:
        # Generate a secure random key
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

def get_master_password():
    master_pwd = input("Enter your master password for this session: ")
    return master_pwd

def add(master_pwd, name, pwd):
    salt = b'\x00' * 16 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, 
        salt=salt,
        iterations=390000,
    )
    derived_key = base64.urlsafe_b64encode(kdf.derive(master_pwd.encode() + load_key()))
    fer = Fernet(derived_key)  # Now the derived_key should be 32 bytes
    with open("Password.txt", "a") as f:
        f.write(name + "|" + fer.encrypt(pwd.encode('utf-8')).decode('utf-8') + "\n")

def view(master_pwd):
    passwords = []  # Initialize an empty list
    try:
        with open("Password.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                data = line.rstrip('\r\n')
                if "|" in data:
                    name, passw = data.split("|")
                    # Same key derivation
                    salt = b'\x00' * 16  
                    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
                    derived_key = base64.urlsafe_b64encode(kdf.derive(master_pwd.encode() + load_key()))
                    fer = Fernet(derived_key)
                    try:
                        decrypted_pwd = fer.decrypt(passw.encode('utf-8')).decode('utf-8')
                        passwords.append((name, decrypted_pwd))  # Add to the list
                    except InvalidToken:
                        print("Name: (Encrypted) , Password: (Encrypted)")
                else:
                    continue 
    except FileNotFoundError:
        print("Password file not found!")
    return passwords  # Return the passwords list
                
if __name__ == "__main__":
    create_key()  # Check for and create key.key if necessary
    master_pwd = get_master_password()  # Get master password at the start
    
    while True:
        mode = input("Would you like to add a new password or view existing ones (add, view, q for quit): ").lower()
        if mode == "q":
            break
        elif mode == "add":
            add(master_pwd)
        elif mode == "view":
            view(master_pwd)
        else:
            print("Invalid mode.")
            continue
