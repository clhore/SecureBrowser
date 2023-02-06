#!/usr/bin/python3

# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

# library
# from tkinter import Tk, Frame, Label, Entry, Button, PhotoImage, messagebox
import threading
import sys
import platform

# custom library
from mymodule.app import create_master_key, encrypt_windows, decrypt_windows
from mymodule import browser, JSON, SecureBrowserMonitor


def check_linux_os_system():
    if platform.system().lower() == "windows":
        sys.exit(1)
    return True


def start_browser(object_browser: object):
    object_browser.exec_browser()


def process_browser_status(object_browser: object):
    object_browser.process_browser_status()


def flag_check(flag: str):
    if flag == '-d': return decrypt_windows.main()[0]
    elif flag == '-e': return encrypt_windows.main()
    elif flag == '-c': return create_master_key.main()
    return None


def start_decrypt_secure_browser():
    # Windows app
    check_code_decrypt, string_password = decrypt_windows.main()

    # Error decrypt files
    if not check_code_decrypt: sys.exit(1)

    return string_password


def start_secure_browser():
    # Create browser object
    secure_browser = browser.Browser(
        browser=JSON.JSON(file='/opt/SecureBrowser/data/config.json').read()['browser']
    )

    # Start browser
    thread_browser = threading.Thread(target=start_browser(secure_browser))
    thread_browser.start()
    thread_browser.join()


def start_monitor_browser_status(encrypt_password):
    # Check status secure_browser
    # thread_check = threading.Thread(target=process_browser_status(secure_browser))
    # thread_check.start()
    thread_monitor = threading.Thread(target=SecureBrowserMonitor.main(encrypt_password))
    thread_monitor.start()
    thread_monitor.join()


def main():
    if len(sys.argv) > 1: flag_check(sys.argv[1]); sys.exit(0)
    if JSON.JSON(file='/opt/SecureBrowser/data/config.json').read()['check_code']:
        encrypt_password = start_decrypt_secure_browser()
        start_secure_browser()
        start_monitor_browser_status(encrypt_password=encrypt_password)


if __name__ == '__main__':
    # Linux's system check
    check_linux_os_system()
    # Start program
    main()
