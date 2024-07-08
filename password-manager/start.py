import pandas as pd
from logic import *
import pytermgui as ptg
import sys


def mainWindow(manager, addAccount):
    container = ptg.Container(
        ptg.Button('Add Account', lambda *_: manager.add(addAccount)),
        ptg.Button('Read Password', lambda *_: print("Printing Password")),
        ptg.Button('Exit', lambda *_: manager.stop()),
    )
    return ptg.Window(container).set_title("Password Manager").center()


def addWindow(manager, file):
    website = ptg.InputField(prompt='website:')
    account = ptg.InputField(prompt='account:')
    password = ptg.InputField(prompt='password:')
    access_key = ptg.InputField(prompt='access_key:')

    container = ptg.Container(
        website, account, password, access_key,
        ptg.Button(
            'Submit', lambda *_: add_password(
                manager, file, str(website.value + '/' + account.value),
                password.value, access_key.value)),
        ptg.Button('Exit', lambda *_: manager.stop()))
    return ptg.Window(container).set_title("Password Manager").center()


def start():
    file = pd.read_csv("passwords.csv", header=0)
    with ptg.WindowManager() as manager:
        addAccount = addWindow(manager, file)
        window = mainWindow(manager, addAccount)
        manager.add(window)
        manager.run()
    manager.stop()


if __name__ == '__main__':
    sys.exit(start())
