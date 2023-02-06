# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

# library
import subprocess
import psutil


class Browser:
    def __init__(self, browser: str = 'firefox'):
        self.browser = browser

    def exec_browser(self):
        try:
            cmd = f'{self.browser} & echo $! > /tmp/.python.browser.tmp & disown'
            subprocess.run(cmd, shell=True)
            return True
        except:
            return False
        return False

    def process_browser_status(self, pid=None):
        if pid is None: pid = self.read_browser_pid()
        if pid in psutil.pids(): return True
        return False

    @staticmethod
    def read_browser_pid():
        return eval(open('/tmp/.python.browser.tmp', 'r').read())