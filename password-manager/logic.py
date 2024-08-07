import pandas as pd
import base64, secrets
from cryptography.fernet import Fernet
import pyperclip


def decrypt(access_key: str, encrypted_password: str) -> str:
    key = base64.b64encode(f"{access_key:<32}".encode("utf-8"))
    password_encryptor = Fernet(key=key)
    try:
        return password_encryptor.decrypt(
            encrypted_password.encode('utf-8')).decode("utf-8")
    except Exception:
        print("invalid password")
        return ""


def encrypt(access_key: str, user_password: str) -> bytes:

    key = base64.b64encode(f"{access_key:<32}".encode("utf-8"))
    password_encryptor = Fernet(key=key)
    return password_encryptor.encrypt(user_password.encode("utf-8"))


def add_password(file: pd.DataFrame, account: str, password: str,
                 access_key: str) -> str:
    if password == '':
        password = secrets.token_urlsafe(13)
    encrypted_password = encrypt(access_key, password)
    file_entry = pd.DataFrame({
        "account": [account],
        'password': [encrypted_password]
    })

    file = pd.concat([file, file_entry], ignore_index=True)
    file.to_csv('passwords.csv', index=False)
    return "Account added successfuly"


def read_password(file: pd.DataFrame, account: int, access_key: str) -> str:
    encrypted_password = file.at[account, 'password'].rsplit("'")[1]
    decrypted_password = decrypt(access_key, encrypted_password)
    pyperclip.copy(decrypted_password)
    return decrypted_password


def change_password(file: pd.DataFrame, name: int, new_password: str,
                    access_key: str) -> str:
    encrypted_pasword = encrypt(access_key, new_password)
    file.at[name, 'password'] = encrypted_pasword

    #I do not return the file but save it instead because I need the main IU function to load it again
    file.to_csv('passwords.csv', index=False)
    return "Password changed successfuly"


def delete_password(file: pd.DataFrame, name: int) -> str:
    file.drop([name], inplace=True)
    print(file)

    file.to_csv('passwords.csv', index=False)
    return "Account Deleted successfuly"


'''
def main():
    if "passwords.csv" not in os.listdir():
        f = open("passwords.csv", 'a')
        f.write("account,password")
        f.close()
    file = pd.read_csv("passwords.csv", header=0)
    print(
        "\n1/A)add account+password\n2/R)Read password\n3/C)Change passwordn\n4/D)Delete password\n"
    )
    option = input("option:")
    match option:
        case "1" | "A" | "a":

            website = input("website:")
            account = website + '/' + input("account:")
            password = input('account password:')
            access_key = input(
                "encryption key can be any string or password that you remember\naccess key:"
            )

            add_password(file, account, password, access_key)
        case "2" | "R" | "r":

            print(file['account'])
            account = int(input('account index :'))

            access_key = input('access key: ')
            read_password(file, account, access_key)

        case "3" | "C" | 'c':

            print(file['account'])
            name = int(input("index:"))
            new_password = input("new password:")
            access_key = input("access key:")
            change_password(file, name, new_password, access_key)
        case "4" | "D" | 'd':

            print(file['account'])
            name = int(input("index:"))
            delete_password(file, name)



if __name__ == '__main__':
    sys.exit(main())
    '''
