import pandas as pd
from logic import *
import pytermgui as ptg
import sys


class passwordManager():

    def __init__(self):

        if "passwords.csv" not in os.listdir():
            f = open("passwords.csv", 'a')
            f.write("account,password")
            f.close()
        self.file = pd.read_csv("passwords.csv", header=0)
        self.open_windows = []
        with ptg.WindowManager() as self.manager:
            changeAccount = self.changeWindow()
            readAccount = self.readWindow()
            addAccount = self.addWindow()
            self.window = self.mainWindow(addAccount, readAccount,
                                          changeAccount)
            self.manager.add(self.window)
            self.manager.run()

    def mainWindow(self, addAccount, readWindow, changeAccount):
        container = ptg.Container(
            ptg.Button('Add Account',
                       lambda *_: self.switch_window(addAccount)),
            ptg.Button('Read Password',
                       lambda *_: self.switch_window(readWindow)),
            ptg.Button('Change Password',
                       lambda *_: self.switch_window(changeAccount)),
            ptg.Button('Exit', lambda *_: self.manager.stop()),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    def singleTextWindow(self, message):
        container = ptg.Container(
            ptg.Label(message),
            ptg.Button("Return", lambda *_: self.switch_window(self.window)),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    def displayPassword(self, password, accountName):
        nameLable = ptg.Label("name: " + accountName)
        if password == '':
            password = 'Invalid access key'
        passwordLable = ptg.Label("password: " + password)
        container = ptg.Container(
            nameLable,
            passwordLable,
            ptg.Label(""),
            ptg.Button('Exit', lambda *_: self.switch_window(self.window)),
        )

        return ptg.Window(container).set_title("Password Manager").center()

    def getPassword(self, account):
        account_lable = ptg.Label(self.file.at[account, 'account'])
        access_key = ptg.InputField(prompt='access_key:')
        container = ptg.Container(
            account_lable, access_key,
            ptg.Button(
                "Submit Password", lambda *_: self.switch_window(
                    self.displayPassword(
                        read_password(self.file, account, access_key.value),
                        self.file.at[account, 'account']))))
        return ptg.Window(container).set_title("Password Manager").center()

    def readWindow(self):

        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: self.switch_window(
                        self.getPassword(account_index))))
        container = ptg.Container(*buttonList)

        return ptg.Window(container).set_title("Password Manager").center()

    def addWindow(self):
        website = ptg.InputField(prompt='website:')
        account = ptg.InputField(prompt='account:')
        password = ptg.InputField(prompt='password:')
        access_key = ptg.InputField(prompt='access key:')

        container = ptg.Container(
            website, account, password, access_key, ptg.Label(""),
            ptg.Button(
                'Submit', lambda *_: self.singleTextWindow(
                    add_password(self.file,
                                 str(website.value + '/' + account.value),
                                 password.value, access_key.value))),
            ptg.Button('Exit', lambda *_: self.manager.stop()))
        return ptg.Window(container).set_title("Password Manager").center()

    #window that can be used whenever I need to announce something happened

    def changePassword(self, account_index):
        accountLable = ptg.Label(self.file.at[account_index, 'account'])
        passwordInputField = ptg.InputField(prompt='New Password:')
        accessKeyInputField = ptg.InputField(prompt='access key:')
        container = ptg.Container(
            accountLable, passwordInputField, accessKeyInputField,
            ptg.Button(
                "Submit", lambda *_: self.switch_window(
                    self.singleTextWindow(
                        change_password(self.file, account_index,
                                        passwordInputField.value,
                                        accessKeyInputField.value)))))
        return ptg.Window(container).set_title("Password Manager").center()

    def changeWindow(self):

        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: self.switch_window(
                        self.changePassword(account_index))))
        container = ptg.Container(*buttonList)
        return ptg.Window(container).set_title("Password Manager").center()

    def switch_window(self, new_window):
        # Close all open windows before adding the new one
        for window in self.open_windows:
            self.manager.remove(window)
        self.open_windows.clear()

        self.manager.add(new_window)
        self.manager.focus(new_window)
        self.open_windows.append(new_window)


if __name__ == '__main__':
    myPasswordManager = passwordManager()
