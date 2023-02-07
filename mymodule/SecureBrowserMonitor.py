#!/usr/bin/python3

# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

from mymodule import browser, crypto, JSON
from mymodule.app import encrypt_windows
import time


def process_secure_browser_status(browser_object: object, pid: int):
    browser_status = browser_object.process_browser_status(pid=pid)
    if browser_status:
        time.sleep(2)
        process_secure_browser_status(browser_object=browser_object, pid=pid)
    return False


def main(password):
    SecureBrowser = browser.Browser()
    if not process_secure_browser_status(SecureBrowser, SecureBrowser.read_browser_pid()):
        #time.sleep(1)# encrypt_windows.EncryptWindows('data/config.json').copy_files()
        crypto.encrypt_file(files=JSON.JSON('/opt/SecureBrowser/data/config.json').read()['files'], string_password=password)
        encrypt_windows.EncryptWindows('/opt/SecureBrowser/data/config.json').copy_files()
        config_file = JSON.JSON('/opt/SecureBrowser/data/config.json')
        config = config_file.read()
        config['check_code'] = True
        config_file.write(config)
