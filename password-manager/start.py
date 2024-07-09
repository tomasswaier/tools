import pandas as pd
import pytermgui as ptg
import os
import base64
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


class passwordManager():

    def __init__(self):

        if "passwords.csv" not in os.listdir():
            f = open("passwords.csv", 'a')
            f.write("account,password")
            f.close()
        self.file = pd.read_csv("passwords.csv", header=0)
        self.open_windows = []
        with ptg.WindowManager() as self.manager:
            self.window = self.mainWindow()
            self.manager.add(self.window)
            self.manager.run()

    def add_password(self, account, password: str, access_key: str) -> str:
        encrypted_password = encrypt(access_key, password)
        file_entry = pd.DataFrame({
            "account": [account],
            'password': [encrypted_password]
        })

        file = pd.concat([self.file, file_entry], ignore_index=True)
        file.to_csv('passwords.csv', index=False)
        return "Account added successfuly"

    def read_password(self, account: int, access_key: str) -> str:
        encrypted_password = self.file.at[account, 'password'].rsplit("'")[1]
        decrypted_password = decrypt(access_key, encrypted_password)
        pyperclip.copy(decrypted_password)
        return decrypted_password

    def change_password(self, name: int, new_password: str,
                        access_key: str) -> str:
        encrypted_pasword = encrypt(access_key, new_password)
        self.file.at[name, 'password'] = encrypted_pasword

        self.file.to_csv('passwords.csv', index=False)
        return "Password changed successfuly"

    def delete_password(self, name: int) -> None:
        self.file.drop([name], inplace=True)

        self.file.to_csv('passwords.csv', index=False)

    def mainWindow(self):
        container = ptg.Container(
            ptg.Button('Add Account',
                       lambda *_: self.switch_window(self.addWindow())),
            ptg.Button('Read Password',
                       lambda *_: self.switch_window(self.readWindow())),
            ptg.Button('Change Password',
                       lambda *_: self.switch_window(self.changeWindow())),
            ptg.Button('Exit', lambda *_: self.manager.stop()),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    #window that can be used whenever I need to announce something happened
    def singleTextWindow(self, message):
        container = ptg.Container(
            ptg.Label(message),
            ptg.Button("Return", lambda *_: self.switch_window(self.window)),
        )
        return ptg.Window(container).set_title("Status").center()

    def displayPassword(self, password, accountName):
        if password == '':
            password = 'Invalid access key'
        passwordLable = ptg.Label("password: " + password)
        container = ptg.Container(
            passwordLable,
            ptg.Label(""),
            ptg.Button("Return", lambda *_: self.switch_window(self.window)),
        )

        return ptg.Window(container).set_title(accountName).center()

    def getPassword(self, account):
        account_lable = ptg.Label(self.file.at[account, 'account'])
        access_key = ptg.InputField(prompt='access_key:')
        container = ptg.Container(
            account_lable, access_key,
            ptg.Button(
                "Submit Password", lambda *_: self.switch_window(
                    self.displayPassword(
                        self.read_password(account, access_key.value), self.
                        file.at[account, 'account']))))

        return ptg.Window(container).set_title("Account Password").center()

    def readWindow(self):
        self.file = pd.read_csv("passwords.csv", header=0)
        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: self.switch_window(
                        self.getPassword(account_index))))
        container = ptg.Container(*buttonList)

        return ptg.Window(container).set_title(
            "Password Manager :Account List(Read)").center()

    def addWindow(self):
        self.file = pd.read_csv("passwords.csv", header=0)
        website = ptg.InputField(prompt='website:')
        account = ptg.InputField(prompt='account:')
        password = ptg.InputField(prompt='password:')
        access_key = ptg.InputField(prompt='access key:')

        container = ptg.Container(
            website, account, password, access_key, ptg.Label(""),
            ptg.Button(
                'Submit', lambda *_: self.switch_window(
                    self.singleTextWindow(
                        self.add_password(
                            str(website.value + '/' + account.value), password.
                            value, access_key.value)))),
            ptg.Button('Exit', lambda *_: self.manager.stop()))
        return ptg.Window(container).set_title(
            "Password Manager :Add Account").center()

    def changePassword(self, account_index):
        accountLable = ptg.Label(self.file.at[account_index, 'account'])
        passwordInputField = ptg.InputField(prompt='New Password:')
        accessKeyInputField = ptg.InputField(prompt='access key:')
        container = ptg.Container(
            accountLable, passwordInputField, accessKeyInputField,
            ptg.Button(
                "Submit", lambda *_: self.switch_window(
                    self.singleTextWindow(
                        self.change_password(account_index, passwordInputField.
                                             value, accessKeyInputField.value))
                )))
        return ptg.Window(container).set_title(
            "Password Manager:Change Password").center()

    def changeWindow(self):

        self.file = pd.read_csv("passwords.csv", header=0)
        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: self.switch_window(
                        self.changePassword(account_index))))
        container = ptg.Container(*buttonList)
        return ptg.Window(container).set_title(
            "Password Manager :Account List(Change)").center()

    def switch_window(self, new_window):
        # Close all open windows before adding the new one
        for window in self.open_windows:
            if window != self.window:
                self.manager.remove(window)
        self.open_windows.clear()

        self.manager.add(new_window)
        self.manager.focus(new_window)
        self.open_windows.append(new_window)


if __name__ == '__main__':
    myPasswordManager = passwordManager()
