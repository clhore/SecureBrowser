# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

# library
from tkinter import Tk, Frame, Label, Entry, Button, PhotoImage, messagebox

# custom library
from mymodule import crypto, JSON


class EncryptWindows:
    def __init__(self, config_file):
        self.config_file = JSON.JSON(config_file)
        self.root_windows = self.create_root_windows(title='SignUp')
        self.title = {'text': 'Encrypt Files', 'x': 88, 'y': 100}
        self.encrypt_file_status = False

    def update_config_file(self, config):
        self.config_file.write(config)

    def copy_files(self, files: list = None):
        if files is None: files = self.config_file.read()['files']
        for file in files:
            file_content = open(file, 'rb').read()
            open(
                f'{self.config_file.read()["session_path"]}{file.split("/").pop()}',
                'wb'
            ).write(file_content)

    def kill_root_windows(self):
        self.root_windows.quit()

    def encrypt_file_windows(self):
        def __check_password__():
            check_code = self.check_input_password(
                    crypto.create_hash_master_key(
                        password_string=password.get()
                    ),
                    self.config_file.read()['master_key_hash']
            )

            if not check_code:
                self.create_error_windows(
                    title='Master Key Error', error_text='The master password is incorrect'
                )
                return False

            try:
                check_code = self.encrypt_file(string_password=password.get()) and self.config_file.read()['verbose']
                if check_code:
                    messagebox.showinfo(
                        message='Files encrypt correctly', title='Encrypt'
                    )
                self.copy_files()
                self.kill_root_windows()
                return True
            except:
                self.create_error_windows(
                    title='Decrypt Error', error_text='Error encrypt files'
                )
                return False

        frame = Frame(
            self.root_windows, bg='#fff', width=350, height=390
        )
        frame.place(x=400, y=50)

        Label(
            frame, text=self.title['text'],
            fg='#57a1f8', bg='#fff',
            font=('Microsoft Yauheni UI Light', 23, 'bold')
        ).place(x=self.title['x'], y=self.title['y'])

        # Input password
        def __on_enter__(e):
            password.delete(0, 'end')

        def __on_leave__(e):
            if password.get() != '':
                __check_password__(); return True
            password.insert(0, 'Password')

        password = Entry(
            frame,
            borderwidth=0, highlightthickness=0,
            width=25, border=0, show="*",
            fg='#000', bg='#fff',
            font=('Microsoft Yauheni UI Light', 11)
        )
        password.place(x=80, y=190)
        password.insert(0, 'Password')
        password.bind('<FocusIn>', __on_enter__)
        password.bind('<FocusOut>', __on_leave__)

        Frame(frame, width=295, height=2, bg='#000').place(x=80, y=220)

        # Button encrypt
        Button(
            frame, justify="center",
            borderwidth=0, highlightthickness=0,
            width=39, height=1,
            text='SUBMIT',
            pady=8, border=1,
            bg='#57a1f8', fg='#fff',
            command=__check_password__
        ).place(x=80, y=250)

        Label(
            frame, text='by Adrián Luján Muñoz (aka clhore)',
            fg='#000', bg='#fff',
            font=('Arial', 9)
        ).place(x=110, y=300)

    def encrypt_file(self, string_password: str, files: list = None):
        if self.config_file.read()['check_code']: return True
        try:
            if files is None: files = self.config_file.read()['files']
            CRYT = crypto.CRYPTO()
            for file in files:
                crypto.write_file(CRYT.encrypt_string(
                    string=crypto.content_file(file=file),
                    password=bytes(string_password, encoding='utf-8')
                ), file)
            config = self.config_file.read()
            config['check_code'] = True
            self.update_config_file(config)
            self.encrypt_file_status = config['check_code']
            return config['check_code']
        except: return False

    def mainloop(self):
        img = PhotoImage(file='data/img/login.png')
        img2 = PhotoImage(file='data/img/tertiaoptio-logo.png')
        Label(self.root_windows, image=img, border=0, bg='#fff').place(x=50, y=140)
        Label(self.root_windows, image=img2, border=0, bg='#fff').place(x=190, y=0)
        self.root_windows.mainloop()
        return self.encrypt_file_status

    @staticmethod
    def create_root_windows(title=str(), geometry='800x400'):
        root_windows = Tk()
        root_windows.title(title)
        root_windows.geometry(geometry)
        root_windows.configure(bg='#fff')
        root_windows.resizable(False, False)
        return root_windows

    @staticmethod
    def create_error_windows(title: str = None, geometry='500x120', error_text: str = None):
        if title is None: title = ''
        if error_text is None: return False
        error_windows = Tk()
        error_windows.title(title)
        error_windows.geometry(geometry)
        error_windows.configure(bg='#423f3e')
        error_windows.resizable(False, False)
        Label(
            error_windows, text=title, fg='#f00', bg='#423f3e',
            font=('Microsoft Yauheni UI Light', 11, 'bold')
        ).place(x=20, y=20)

        width_height = geometry.split('x')
        frame_width = eval(width_height[0])-40; frame_height = eval(width_height[1])-70
        frame = Frame(
            error_windows, bg='#1a1716', width=frame_width, height=frame_height,
        ); frame.place(x=20, y=50)
        Label(
            frame, text=error_text, fg='#fff', bg='#1a1716'
        ).place(x=1.5, y=1.5)
        return error_windows

    @staticmethod
    def create_master_key(password: str):
        pass

    @staticmethod
    def check_input_password(hash_password: str = None, hash_master_password: str = None):
        if hash_password is None or hash_master_password is None: return False
        if hash_password == hash_master_password: return True
        return False

    @staticmethod
    def create_frame(windows, color=None, xy=None, width=350, height=390):
        if xy is None: xy = [400, 50]
        if color is None: color = '#000'
        return Frame(
            windows,
            width=width, height=height,
            bg=color
        ).place(x=xy[0], y=xy[1])


# main function
def main():
    app = EncryptWindows(config_file='/opt/SecureBrowser/data/config.json')
    app.encrypt_file_windows()
    return app.mainloop()