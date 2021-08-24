'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-23
Version: 0.0.0
'''

# __LYBRARIES__ #
from tkinter import *


# __MAIN CODE__ #
class Main_Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self._frame = Main_Frame(self)
        self._frame.pack(fill=NONE, expand=1)

        self.title('Contabilidad Zotz')
        self.iconbitmap('files/logo.ico')
        self.geometry('1280x960')
        self.resizable(FALSE, FALSE)


class Main_Frame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self._master = master


def run():
    main = Main_Window()
    main.mainloop()


if __name__ == '__main__':
    run()

# __NOTES__ #
'''

'''

# __BIBLIOGRAPHY__ #
'''

'''
