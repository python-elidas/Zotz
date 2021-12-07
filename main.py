'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-23
Version: 0.0.0
'''

# __LYBRARIES__ #
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import os as file
import openpyxl as xls
from siguiente import Excel


# __MAIN CODE__ #
class Main_Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self._frame = Main_Frame(self)
        self._frame.pack(fill=NONE, expand=1)

        self.title('Contabilidad Zotz')
        self.iconbitmap('files/logo.ico')
        self.geometry('600x250')
        self.resizable(FALSE, FALSE)
        
    def run(self):
        dir = self._frame.folder.get()
        bills = file.listdir(dir)
        excel = self._frame.excel.get()
        # Comprobamos que facturas han sido pasadas para no repetir
        process = list()
        for bil in bills:
            nme = bil.split('.')[0].replace('-MAKRO', '')
            if '.pdf' in bil and not nme in self._frame.ws_nms:
                process.append(bil)
        self.switch_frames(Info)
        Label(self._frame, text='Procesando Archivos...')\
            .grid(row=3)
        try:
            for bil in process:
                pdf = dir.replace('C:', '//') + '/' + bil
                Label(self._frame, text=f'{pdf}')
                Excel(excel, pdf)
                process.pop(process.index(bil))
        except PermissionError:
            messagebox.showerror(
                message="Cierra el fichero Excel y vuelve a intentarlo",
                title="Permission Error"
            )
            self.run()
        
    def switch_frames(self, frame):
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame(self)
        self._frame.pack(fill=NONE, expand=1)


class Main_Frame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self._master = master

        Label(self, text='Selecciona la carpeta de las facturas')\
            .grid(row=0, column=0, sticky=W)
        self.folder = Entry(self, width=30)
        self.folder.grid(row=1, column=0, sticky=W)
        self.f_b = Button(self, text='···', width=3, command=self.select_folder)
        self.f_b.grid(row=1, column=1)

        Label(self, text='Selecciona el Excel')\
            .grid(row=0, column=2, sticky=W, padx=10)
        self.excel = Entry(self, width=35)
        self.excel.grid(row=1, column=2, sticky=W, padx=10)
        self.f_e = Button(self, text='···', width=3, command=self.select_excel)
        self.f_e.grid(row=1, column=3, sticky=E)

        self.exe = Button(self, text='Run', command=self._master.run)
        self.exe.grid(row=2, column=3, sticky=E, pady=10)

    def select_excel(self):
        if self.folder.get() == '':
            init = '/'
        else:
            init = self.folder.get()
            init = '/'.join(init.split('/')[:-1])
        xcel = filedialog.askopenfilename(
            initialdir=init,
            title='Selecciona el Libro de Excel',
            filetypes=(("Excel files", "*.xlsx; *.xls"),)
        )
        self.excel.delete(0, END)
        self.excel.insert(0, xcel)
        wb = xls.load_workbook(self.excel.get(), read_only=True)
        self.ws_nms = list(wb.sheetnames)

    def select_folder(self):
        dir = filedialog.askdirectory()
        self.folder.delete(0, END)
        self.folder.insert(0, dir)


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
    · ProgressBar: https://recursospython.com/guias-y-manuales/barra-de-progreso-progressbar-tcltk-tkinter/

'''
