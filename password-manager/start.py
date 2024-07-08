import pandas as pd
from logic import *
import pytermgui as ptg
import sys


def mainWindow(manager, addAccount, readWindow):
    container = ptg.Container(
        ptg.Button('Add Account', lambda *_: manager.add(addAccount)),
        ptg.Button('Read Password', lambda *_: manager.add(readWindow)),
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
    access_key = ptg.InputField(prompt='access_key:')

    container = ptg.Container(
        website, account, password, access_key, ptg.Label(""),
        ptg.Button(
            'Submit', lambda *_: add_password(
                manager, file, str(website.value + '/' + account.value),
                password.value, access_key.value)),
        ptg.Button('Exit', lambda *_: manager.stop()))
    return ptg.Window(container).set_title("Password Manager").center()


def start():
    file = pd.read_csv("passwords.csv", header=0)
    with ptg.WindowManager() as manager:
        readAccount = readWindow(manager, file)
        addAccount = addWindow(manager, file)
        window = mainWindow(manager, addAccount, readAccount)
        manager.add(window)
        manager.run()
    manager.stop()


if __name__ == '__main__':
    sys.exit(start())
