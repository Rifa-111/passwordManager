import os
import json
import getpass
from cryptography.fernet import Fernet
import base64

# Initialize cryptography
def init_cryptography(key_file):
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as key_file:
            key_file.write(key)

    with open(key_file, 'rb') as key_file:
        key = key_file.read()

    return Fernet(key)

# Encrypt and decrypt functions
def encrypt(data, cipher_suite):
    return cipher_suite.encrypt(data.encode())

def decrypt(encrypted_data, cipher_suite):
    return cipher_suite.decrypt(encrypted_data).decode()

# Main password manager
def main():
    key_file = "key.key"
    cipher_suite = init_cryptography(key_file)

    try:
        with open("passwords.json", "r") as password_file:
            passwords = json.load(password_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        passwords = {}

    while True:
        print("\nOptions:")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            account_name = input("Enter the account name: ")
            password = getpass.getpass("Enter the password: ")

            # Encrypt the password before storing it and encode it as base64
            encrypted_password = base64.b64encode(encrypt(password, cipher_suite)).decode()

            passwords[account_name] = encrypted_password
            with open("passwords.json", "w") as password_file:
                json.dump(passwords, password_file)

        elif choice == "2":
            account_name = input("Enter the account name: ")
            if account_name in passwords:
                # Decode from base64 and then decrypt and display the password
                encrypted_password = base64.b64decode(passwords[account_name])
                decrypted_password = decrypt(encrypted_password, cipher_suite)
                print(f"Password for {account_name}: {decrypted_password}")
            else:
                print("Account not found.")

        elif choice == "3":
            break

if __name__ == "__main__":
    main()
