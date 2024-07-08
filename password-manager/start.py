import pandas as pd
from logic import *
import pytermgui as ptg
import sys


def mainWindow(manager, addAccount, readWindow, changeAccount):
    container = ptg.Container(
        ptg.Button('Add Account', lambda *_: manager.add(addAccount)),
        ptg.Button('Read Password', lambda *_: manager.add(readWindow)),
        ptg.Button('Change Password', lambda *_: manager.add(changeAccount)),
        ptg.Button('Exit', lambda *_: manager.stop()),
    )
    return ptg.Window(container).set_title("Password Manager").center()


def displayPassword(manager, password, accountName):
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


def getPassword(manager, file, account):
    account_lable = ptg.Label(file.at[account, 'account'])
    access_key = ptg.InputField(prompt='access_key:')
    container = ptg.Container(
        account_lable, access_key,
        ptg.Button(
            "Submit Password", lambda *_: manager.add(
                displayPassword(manager,
                                read_password(file, account, access_key.value),
                                file.at[account, 'account']))))
    return ptg.Window(container).set_title("Password Manager").center()


def readWindow(manager, file):

    buttonList = []
    for account_index in range(file.shape[0]):
        buttonList.append(
            ptg.Button(
                file.at[account_index, 'account'], lambda *_: manager.add(
                    getPassword(manager, file, account_index))))
    container = ptg.Container(*buttonList)

    return ptg.Window(container).set_title("Password Manager").center()


def addWindow(manager, file):
    website = ptg.InputField(prompt='website:')
    account = ptg.InputField(prompt='account:')
    password = ptg.InputField(prompt='password:')
    access_key = ptg.InputField(prompt='access key:')

    container = ptg.Container(
        website, account, password, access_key, ptg.Label(""),
        ptg.Button(
            'Submit', lambda *_: add_password(
                manager, file, str(website.value + '/' + account.value),
                password.value, access_key.value)),
        ptg.Button('Exit', lambda *_: manager.stop()))
    return ptg.Window(container).set_title("Password Manager").center()


#window that can be used whenever I need to announce something happened
def singleTextWindow(manager, message):
    container = ptg.Container(
        ptg.Label(message),
        ptg.Button("Return", lambda *_: print('xd')),
    )
    return ptg.Window(container).set_title("Password Manager").center()


def changePassword(manager, file, account_index):
    accountLable = ptg.Label(file.at[account_index, 'account'])
    passwordInputField = ptg.InputField(prompt='New Password:')
    accessKeyInputField = ptg.InputField(prompt='access key:')
    container = ptg.Container(
        accountLable, passwordInputField, accessKeyInputField,
        ptg.Button(
            "Submit", lambda *_: manager.add(
                singleTextWindow(
                    manager,
                    change_password(file, account_index, passwordInputField.
                                    value, accessKeyInputField.value)))))
    return ptg.Window(container).set_title("Password Manager").center()


def changeWindow(manager, file):

    buttonList = []
    for account_index in range(file.shape[0]):
        buttonList.append(
            ptg.Button(
                file.at[account_index, 'account'], lambda *_: manager.add(
                    changePassword(manager, file, account_index))))
    container = ptg.Container(*buttonList)
    return ptg.Window(container).set_title("Password Manager").center()


def start():
    file = pd.read_csv("passwords.csv", header=0)
    with ptg.WindowManager() as manager:
        changeAccount = changeWindow(manager, file)
        readAccount = readWindow(manager, file)
        addAccount = addWindow(manager, file)
        window = mainWindow(manager, addAccount, readAccount, changeAccount)
        manager.add(window)
        manager.run()
    manager.stop()


if __name__ == '__main__':
    sys.exit(start())
