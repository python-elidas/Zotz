'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-23
Version: 1.3.0
'''

# __LYBRARIES__ #
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import os as file
import simply_sqlite as sSQL
import openpyxl as xls
from siguiente import Excel
import threading as th
import time



# __MAIN CODE__ #
class Main_Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.ind = 0
        self.n, self.m = 1, 2
        
        self.exe = th.Thread(target=self.run)

        self._frame = Main_Frame(self)
        self._frame.pack(fill=NONE, expand=1)

        self.title('Contabilidad Zotz')
        self.iconbitmap('files/logo.ico')
        self.geometry('600x250')
        self.resizable(FALSE, FALSE)
        
        self.exit = Button(self, text = 'Salir', command = self.out)
        self.exit.pack(anchor = SE, side = BOTTOM, padx = 10, pady = 5)
    
    def out(self):
        self.kill_thread()
        self.destroy()
    
    def kill_thread(self):
        if self.exe.is_alive():
            self.exe.join()
        
    def run(self):
        # modificamos la ventana para adaptarse a la nueva información
        self.geometry('600x275')
        
        # Obtenemos la información del campo y deshabilitamos el campo y boton
        dir = self._frame.folder.get()
        self._frame.folder['state'] = 'disabled'
        self._frame.f_b['state'] = 'disabled'
        
        # Obtenemos la información del campo y deshabilitamos el campo y boton
        bills = file.listdir(dir)
        excel = self._frame.excel.get()
        self._frame.excel['state'] = 'disabled'
        self._frame.f_e['state'] = 'disabled'
        
        # Empezamos a mostrar nueva información y creamos la barra de progreso
        Label(self._frame, text='Procesando Archivos...')\
            .grid(row=2, column=0, sticky=W)
        self.p_b = Progressbar(self._frame, length=500)
        self.p_b.grid(row=3, columnspan=4)
        
        # Comprobamos que facturas han sido pasadas para no repetir
        process = list()
        for bil in bills:
            nme = bil.split('.')[0].split(' - ')[-1]
            if '.pdf' in nme:
                nme = nme.replace('.pdf', '')
            if '.pdf' in bil and not nme in self._frame.ws_nms:
                process.append(bil)
                
        # Establecemos el maximo de la barra de progreso
        self.p_b.config(maximum=len(process))
        
        # Empezamos a leer y convertir información
        try:
            self.n, self.m = 0, len(process)
            # Iteramos por todas las facturas
            for self.bil in process:
                # adecuamos el nombre del archivo
                pdf = dir.replace('C:', '//') + '/' + self.bil
                # mostramos mas infromacion
                Label(self._frame,
                      text=f'{self.n} de {self.m}')\
                    .grid(row=2, column=2)                    
                Label(self._frame, 
                        text=f'Archivo {self.bil}')\
                    .grid(row=4, column=0, columnspan=3, sticky=W)
                Label(self._frame,
                        text='\tLeyendo Archivo')\
                    .grid(row=5, column=0, sticky=W)
                Label(self._frame,
                        text='\tCreando Hoja')\
                    .grid(row=6, column=0, sticky=W)
                Label(self._frame,
                        text='\tEscribiendo')\
                    .grid(row=7, column=0, sticky=W)
                Excel(excel, pdf, self)
                self.n += 1
                self.p_b.step(1)
                # time.sleep(2)
            # Una vez finalizado, avisamos.
            messagebox.showinfo(
                message="El archivo Excel ha sido actualizado.\n reinicie el programa para procesar mas archivos.",
                title="Porceso completado.")
            self._frame.exe.config(text='Apagar', command=self.out)
        # si esta el excel abierto
        except PermissionError:
            messagebox.showerror(
                message="Cierra el fichero Excel y vuelve a intentarlo",
                title="Permission Error"
            )
            self.run()
        # si se produce cualquier error
        except Exception as e:
            messagebox.showerror(
                title=type(e).__name__,
                message=f'Ha ocurrido un error.\
                \nPor favor contacte con el SAT y facilite la siguiente información:\
                \n\t{e}\
                \nAsí como el nombre de este ventana.\
                \n\
                \nFichero: {self.bil}')
        
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

        self.exe = Button(self, text='Run', command=self.exe_run)
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

    def exe_run(self):
        if not self.excel.get() == '' and not self.folder.get() == '':
            self._master.exe.start()
        else:
            messagebox.showerror(
                message="Verifique que ambos campos están complimentados y vuelva a intentarlo",
                title='Campo vacío'
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
    · ProgressBar: https://recursospython.com/guias-y-manuales/barra-de-progreso-progressbar-tcltk-tkinter/

'''
