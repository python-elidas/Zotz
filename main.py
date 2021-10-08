'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-23
Version: 0.0.0
'''

# __LYBRARIES__ #
from tkinter import *
from tkinter import filedialog
import os as file
from siguiente import Excel


# __MAIN CODE__ #
class Main_Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self._frame = Main_Frame(self)
        self._frame.pack(fill=NONE, expand=1)

        self.title('Contabilidad Zotz')
        self.iconbitmap('files/logo.ico')
        self.geometry('500x200')
        self.resizable(FALSE, FALSE)


class Main_Frame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self._master = master

        Label(self, text='Selecciona la carpeta de las facturas')\
            .grid(row=0, column=0, sticky=W)
        self.folder = Entry(self, width=30)
        self.folder.grid(row=1, column=0, sticky=W)
        self.f_b = Button(self, text='···', command=self.select_folder)
        self.f_b.grid(row=1, column=1)

        Label(self, text='Selecciona el Excel')\
            .grid(row=0, column=2, sticky=W, padx=10)
        self.excel = Entry(self, width=35)
        self.excel.grid(row=1, column=2, sticky=W, padx=10)
        self.f_e = Button(self, text='···', command=self.select_excel)
        self.f_e.grid(row=1, column=3, sticky=E)

        self.exe = Button(self, text='Run', command=self.run)
        self.exe.grid(row=2, column=3, sticky=E, pady=10)

    def select_excel(self):
        if self.folder.get() == '':
            init = '/'
        else:
            init = self.folder.get()
        xcel = filedialog.askopenfilename(
            initialdir=init,
            title='Selecciona el Libro de Excel',
            filetypes=(("Excel files", "*.xlsx; *.xls"),)
        )
        self.excel.delete(0, END)
        self.excel.insert(0, xcel)

    def select_folder(self):
        dir = filedialog.askdirectory()
        self.folder.delete(0, END)
        self.folder.insert(0, dir)

    def run(self):
        dir = self.folder.get()
        bills = file.listdir(dir)
        try:
            for bil in bills:
                pdf = dir.replace('C:', '//') + '/' + bil
                Excel(self.excel.get(), pdf)
        except PermissionError:
            messagebox.showerror(
                message="Cierra el fichero Excel y vuelve a intentarlo",
                title="Permision Error"
            )


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
