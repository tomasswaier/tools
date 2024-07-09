import pandas as pd
import pytermgui as ptg
import os
from logic import add_password, read_password, change_password, delete_password


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
            self.switch_window(self.window)
            self.manager.run()

    def delete_password(self, name: int) -> None:
        self.file.drop([name], inplace=True)

        self.file.to_csv('passwords.csv', index=False)

    def mainWindow(self):

        self.file = pd.read_csv("passwords.csv", header=0)
        container = ptg.Container(
            ptg.Button('Add Account',
                       lambda *_: self.switch_window(self.addWindow())),
            ptg.Button('Read Password',
                       lambda *_: self.switch_window(self.readWindow())),
            ptg.Button('Change Password',
                       lambda *_: self.switch_window(self.changeWindow())),
            ptg.Button('Delete Account',
                       lambda *_: self.switch_window(self.deleteWindow())),
            ptg.Button('Exit', lambda *_: self.manager.stop()),
        )
        return ptg.Window(container).set_title("Password Manager").center()

    #window that can be used whenever I need to announce something happened
    def singleTextWindow(self, message, title):
        container = ptg.Container(
            ptg.Label(message),
            #need to call new instance of the mainWindow for passswords.csv to refresh
            ptg.Button("Return",
                       lambda *_: self.switch_window(self.mainWindow())),
        )
        return ptg.Window(container).set_title(title).center()

    def getPassword(self, account):
        account_lable = ptg.Label(self.file.at[account, 'account'])
        access_key = ptg.InputField(prompt='access_key:')
        container = ptg.Container(
            account_lable, access_key,
            ptg.Button(
                "Submit Password", lambda *_: self.switch_window(
                    self.singleTextWindow(
                        "Password is copied to clipboard\n" + read_password(
                            self.file, account, access_key.value), "Account :"
                        + self.file.at[account, 'account']))))

        return ptg.Window(container).set_title("Account Password").center()

    def readWindow(self):
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

    def deleteWindow(self):
        buttonList = []
        for account_index in range(self.file.shape[0]):
            buttonList.append(
                ptg.Button(
                    self.file.at[account_index, 'account'],
                    lambda *_: self.switch_window(
                        self.singleTextWindow(
                            delete_password(self.file, account_index),
                            "Deleted Account"))))
        container = ptg.Container(*buttonList)
        return ptg.Window(container).set_title(
            "Password Manager :Account List(Change)").center()

    def addWindow(self):
        website = ptg.InputField(prompt='website:')
        account = ptg.InputField(prompt='account:')
        password = ptg.InputField(prompt='password:')
        access_key = ptg.InputField(prompt='access key:')

        container = ptg.Container(
            website, account, password, access_key, ptg.Label(""),
            ptg.Button(
                'Submit', lambda *_: self.switch_window(
                    self.singleTextWindow(
                        add_password(self.file,
                                     str(website.value + '/' + account.value),
                                     password.value, access_key.value),
                        "Account Added:" + account.value))),
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
                        change_password(
                            self.file, account_index, passwordInputField.value,
                            accessKeyInputField.value), "Password Changed"))))
        return ptg.Window(container).set_title(
            "Password Manager:Change Password").center()

    def changeWindow(self):

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
            self.manager.remove(window)
        self.open_windows.clear()

        self.manager.add(new_window)
        self.manager.focus(new_window)
        self.open_windows.append(new_window)


if __name__ == '__main__':
    myPasswordManager = passwordManager()
