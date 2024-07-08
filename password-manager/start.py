import pandas as pd
from logic import *
import pytermgui as ptg
import sys


class passwordManager():

    def mainWindow(self, manager, addAccount, readWindow, changeAccount):
        container = ptg.Container(
            ptg.Button('Add Account', lambda *_: manager.add(addAccount)),
            ptg.Button('Read Password', lambda *_: manager.add(readWindow)),
            ptg.Button('Change Password',
                       lambda *_: manager.add(changeAccount)),
            ptg.Button('Exit', lambda *_: manager.stop()),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    def displayPassword(self, manager, password, accountName):
        nameLable = ptg.Label("name: " + accountName)
        if password == '':
            password = 'Invalid access key'
        passwordLable = ptg.Label("password: " + password)
        container = ptg.Container(
            nameLable,
            passwordLable,
            ptg.Label(""),
            ptg.Button('Exit', lambda *_: manager.stop()),
        )

        return ptg.Window(container).set_title("Password Manager").center()

    def getPassword(self, manager, account):
        account_lable = ptg.Label(self.file.at[account, 'account'])
        access_key = ptg.InputField(prompt='access_key:')
        container = ptg.Container(
            account_lable, access_key,
            ptg.Button(
                "Submit Password", lambda *_: manager.add(
                    self.displayPassword(
                        manager,
                        read_password(self.file, account, access_key.value),
                        self.file.at[account, 'account']))))
        return ptg.Window(container).set_title("Password Manager").center()

    def readWindow(self, manager):

        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: manager.add(
                        self.getPassword(manager, account_index))))
        container = ptg.Container(*buttonList)

        return ptg.Window(container).set_title("Password Manager").center()

    def addWindow(self, manager):
        website = ptg.InputField(prompt='website:')
        account = ptg.InputField(prompt='account:')
        password = ptg.InputField(prompt='password:')
        access_key = ptg.InputField(prompt='access key:')

        container = ptg.Container(
            website, account, password, access_key, ptg.Label(""),
            ptg.Button(
                'Submit', lambda *_: add_password(
                    manager, self.file, str(website.value + '/' + account.value
                                            ), password.value, access_key.value
                )), ptg.Button('Exit', lambda *_: manager.stop()))
        return ptg.Window(container).set_title("Password Manager").center()

    #window that can be used whenever I need to announce something happened
    def singleTextWindow(self, manager, message):
        container = ptg.Container(
            ptg.Label(message),
            ptg.Button("Return", lambda *_: manager.focus_next(step=1)),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    def changePassword(self, manager, account_index):
        accountLable = ptg.Label(self.file.at[account_index, 'account'])
        passwordInputField = ptg.InputField(prompt='New Password:')
        accessKeyInputField = ptg.InputField(prompt='access key:')
        container = ptg.Container(
            accountLable, passwordInputField, accessKeyInputField,
            ptg.Button(
                "Submit", lambda *_: manager.add(
                    self.singleTextWindow(
                        manager,
                        change_password(self.file, account_index,
                                        passwordInputField.value,
                                        accessKeyInputField.value)))))
        return ptg.Window(container).set_title("Password Manager").center()

    def changeWindow(self, manager):

        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: manager.add(
                        self.changePassword(manager, account_index))))
        container = ptg.Container(*buttonList)
        return ptg.Window(container).set_title("Password Manager").center()

    def __init__(self):

        if "passwords.csv" not in os.listdir():
            f = open("passwords.csv", 'a')
            f.write("account,password")
            f.close()
        self.file = pd.read_csv("passwords.csv", header=0)

        with ptg.WindowManager() as manager:
            changeAccount = self.changeWindow(manager)
            readAccount = self.readWindow(manager)
            addAccount = self.addWindow(manager)
            window = self.mainWindow(manager, addAccount, readAccount,
                                     changeAccount)
            manager.add(window)
            manager.run()
        manager.stop()

    def main(self):
        pass


if __name__ == '__main__':
    myPasswordManager = passwordManager()
