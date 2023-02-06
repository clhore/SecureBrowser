# encoding: utf-8
# autor: Adrian Lujan Munoz (aka clhore)

# library
from tkinter import Tk, Frame, Label, Entry, Button, PhotoImage, messagebox

# custom library
from mymodule import crypto, JSON


class MasterKeyWindows:
    def __init__(self, config_file='data/config.json'):
        self.config_file = JSON.JSON(config_file)
        self.root_windows = self.create_root_windows(title='SignUp')
        self.title = {'text': 'Master Key', 'x': 110, 'y': 100}

    def update_config_file(self, config):
        self.config_file.write(config)

    def kill_root_windows(self):
        self.root_windows.quit()

    def create_password_windows(self):
        def __create_password__():
            if not self.check_input_password(password.get(), confirm_password.get()):
                self.create_error_windows(
                    title='Password Error', error_text='Las contraseñas no coinciden'
                )
                return False

            try:
                password_hash = crypto\
                    .create_hash_master_key(password_string=password.get())
                config = self.config_file.read()
                config['master_key_hash'] = password_hash
                self.update_config_file(config)
                messagebox.showinfo(
                    message='Master password created successfully', title='Master password'
                )
                self.kill_root_windows()
                return True
            except:
                self.create_error_windows(
                    title='Password Error', error_text='Error create master key'
                )
                return False

        frame = Frame(
            self.root_windows, bg='#fff',
            width=350, height=390
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
            print('enter')

        def __on_leave__(e):
            if password.get() == '': password.insert(0, 'Password')
            print('level')

        password = Entry(
            frame,
            borderwidth=0, highlightthickness=0,
            width=25, border=0,
            fg='#000', bg='#fff',
            font=('Microsoft Yauheni UI Light', 11)
        )
        password.place(x=80, y=170)
        password.insert(0, 'Password')
        password.bind('<FocusIn>', __on_enter__)
        password.bind('<FocusOut>', __on_leave__)

        Frame(frame, width=295, height=2, bg='#000').place(x=80, y=200)

        def __on_enter__(e):
            confirm_password.delete(0, 'end')

        def __on_leave__(e):
            if confirm_password.get() != '':
                __create_password__(); return True
            #confirm_password.insert(0, 'Confirm password')

        confirm_password = Entry(
            frame,
            borderwidth=0, highlightthickness=0,
            width=25, border=0,
            fg='#000', bg='#fff',
            font=('Microsoft Yauheni UI Light', 11)
        )
        confirm_password.place(x=80, y=230)
        confirm_password.insert(0, 'Confirm password')
        confirm_password.bind('<FocusIn>', __on_enter__)
        confirm_password.bind('<FocusOut>', __on_leave__)

        Frame(frame, width=295, height=2, bg='#000').place(x=80, y=260)

        # Button encrypt
        Button(
            frame, justify="center",
            borderwidth=0, highlightthickness=0,
            width=39, height=1,
            text='SUBMIT',
            pady=8, border=1,
            bg='#57a1f8', fg='#fff',
            command=__create_password__
        ).place(x=80, y=280)

        Label(
            frame, text='by Adrián Luján Muñoz (aka clhore)',
            fg='#000', bg='#fff',
            font=('Arial', 9)
        ).place(x=110, y=324)

    def mainloop(self):
        img = PhotoImage(file='data/img/login.png')
        img2 = PhotoImage(file='data/img/tertiaoptio-logo.png')
        Label(self.root_windows, image=img, border=0, bg='#fff').place(x=50, y=140)
        Label(self.root_windows, image=img2, border=0, bg='#fff').place(x=190, y=0)
        self.root_windows.mainloop()

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
    def check_input_password(password: str = None, confirm_password: str = None):
        if password is None or confirm_password is None: return False
        if password == confirm_password: return True
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
    app = MasterKeyWindows(config_file='/opt/SecureBrowser/data/config.json')
    app.create_password_windows()
    app.mainloop()