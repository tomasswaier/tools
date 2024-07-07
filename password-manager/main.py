import pandas as pd
import os
import base64
from cryptography.fernet import Fernet


def decrypt(user_password: str, encrypted_password: list[str]) -> str:
    key = base64.b64encode(f"{user_password:<32}".encode("utf-8"))
    password_encryptor = Fernet(key=key)
    return password_encryptor.decrypt(
        encrypted_password[1].encode('utf-8')).decode("utf-8")


def encrypt(user_password: str, encryption_password) -> bytes:

    key = base64.b64encode(f"{encryption_password:<32}".encode("utf-8"))
    password_encryptor = Fernet(key=key)
    return password_encryptor.encrypt(user_password.encode("utf-8"))


def add_password(file: pd.DataFrame):
    website = input("website:")
    account = website + '/' + input("account:")
    password = input('account password:')
    user_password = input(
        "encryption key can be any string or password that you remember\nencryption key:"
    )
    encrypted_password = encrypt(user_password, password)
    file_entry = pd.DataFrame({
        "account": [account],
        'password': [encrypted_password]
    })

    file = pd.concat([file, file_entry], ignore_index=True)
    file.to_csv('passwords.csv', index=False)
    print(file)


#am I supposed to define parameters for pandas ?
def read_password(file: pd.DataFrame):
    print(file['account'])
    account = int(input('account/index :'))

    encrypted_password = file.at[account, 'password'].rsplit("'")
    user_password = input('password: ')
    decrypted_password = decrypt(user_password, encrypted_password)

    print(decrypted_password)


def main():
    if "passwords.csv" not in os.listdir():
        f = open("passwords.csv", 'a')
        f.write("account,password")
        f.close()
    file = pd.read_csv("passwords.csv", header=0)
    print("""\n1/A)add account+password\n2/R)read password\n3/X)exit\n\n""")
    option = input("option:")
    match option:
        case "1" | "A" | "a":
            add_password(file)
        case "2" | "R" | "r":
            read_password(file)


main()
