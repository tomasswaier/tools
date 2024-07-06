import pandas as pd
import os
import base64
from cryptography.fernet import Fernet


def add_password(file: pd.DataFrame, ):
    account = input("account:")
    password = input('account password:')
    user_password = input(
        "encryption key can be any string or password that you remember\nencryption key:"
    )
    key = base64.b85encode(f'{user_password:<32}'.encode('utf-8'))
    password_encryptor = Fernet(key=key)
    encrypted = password_encryptor.encrypt(password.encode('utf-8'))

    print(account, password, encrypted)


def main():
    if "passwords.csv" not in os.listdir():
        f = open("passwords.csv", 'a')
        f.close()
    file = pd.read_csv("passwords.csv",
                       header=None,
                       names=['account', 'password'])
    print("""\n1/A)add account+password\n2/R)read password\n3/X)exit\n\n""")
    option = input("option:")
    match option:
        case "1" | "A" | "a":
            add_password(file)
        case "2" | "R" | "r":
            print("mhm")


main()
