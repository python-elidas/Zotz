'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-26T11:18:58.589Z
Version: 0.0.1
'''

# __LYBRARIES__ #
from tkinter import *
import openpyxl as xls
import simply_sqlite as SQL
from makro import Makro
from datetime import datetime
from sel_type import Sel_Type

# __MAIN CODE__ #
class Excel:
    def __init__(self, xcel, pdf, _master, wb='', new='', bill=''):
        self.wb = wb
        # obtiene la fecha de hoy
        self.today = datetime.now().strftime('%x')
        # accedemos a la base de datos
        self.db = SQL.SQL('files/zotz_db')
        # comprobamos que no se le ha pasado nada...
        if new == '' and bill == '' and wb == '':
            # obtenemos el nombre de la factura y su información
            M = Makro(pdf)
            self.new, self.bill = M.result()  #! generalizar
            # accedemos al excel
            self.wb = xls.load_workbook(filename=xcel, read_only=False)
            # creamos la hoja con la que trabajaremos
            self.ws = self.wb.copy_worksheet(self.wb['Siguiente'])
            # Establecemos el tituo de la nueva hoja
            self.ws.title = self.new
        else:
            self.new, self.bill = new, bill
            self.wb = wb
            self.ws = self.wb[self.new]
            bool = True
        # Comprobamos si existen elementos sin ID
        self.get_id()
        # si existen, pedimos intervencion del usuario
        if not len(self.no_ID) == 0:
            id = Sel_Type(self.no_ID, self.wb, self.new, self.bill)
            id.mainloop()
        # si no, continuamos
        else:
            # Escribimos la cabecera
            self.write_head()
            # Escribimos los articulos:
            self.write_items()
            # Escribimos los descuentos si existen:
            try:
                self.write_discounts()
            except KeyError:
                pass
            # reordenamos el desorden:
            self.reorder() 
            # ejecutamos el siguiente paso:
            self.overview()
            # Guardamos los cambios
            self.wb.save(xcel)
        print(f'Bill {self.new} Saved correctly!')
        _master.ind += 1
        if bool:
            _master.exe.start()

    def write_head(self): # Escribimos los datos relevantes de la factura
        # número de factura y fecha
        try:
            self.ws['G2'] = self.bill['Factura'][0]
            self.ws['G3'] = self.bill['Factura'][1]
            self.ws['G4'] = self.bill['fecha']
        except KeyError:
            self.ws['D2'] = 'Fact. Dev.'
            self.ws['G2'] = self.bill['Factura devolucion'][0]
            self.ws['G3'] = self.bill['Factura devolucion'][1]
            self.ws['G4'] = self.bill['fecha']

    def get_id(self):
        no_ID = list()
        for item in self.bill['articulos']:
            if len(self.db.show_one_row(
                'Articulos', 'Codigo', item['codigo'])) == 0:
                no_ID.append(item)
        if not len(no_ID) == 0:
            pass
            
    def write_items(self): # empezamos con los articulos:
        items = self.bill['articulos']
        self.row = 62
        for item in items:
            # obtenemos la referencia del tipo de producto
            self.ws[f'A{self.row}'] = self.row - 61  # escribimos el numero de la fila
            self.ws[f'B{self.row}'] = item['codigo']  # escribimos la referencia
            self.ws[f'C{self.row}'] = item['desc']  # escribimos la descripción
            self.ws[f'D{self.row}'] = self.db.show_one_row(
                'Articulos', 'Codigo', item['codigo'])[0][2]
            self.ws[f'E{self.row}'] = item['prec ud']
            self.ws[f'F{self.row}'] = item['ud pac']
            self.ws[f'G{self.row}'] = item['precio']
            self.ws[f'H{self.row}'] = item['uds']
            self.ws[f'I{self.row}'] = item['precio'] * int(item['uds'])
            self.ws[f'J{self.row}'] = item['iva']
            
            #Insertamos la siguiente fila:
            self.insert_new_row()

    def insert_new_row(self):
            # insertamos la siguiente fila
            self.ws.insert_rows(self.row+1)
            # cpiamos las formulas pertinentes
            self.ws[f'K{self.row+1}'] = str(self.ws[f'K{self.row}'].value)\
                .replace(str(self.row), str(self.row+1))
            self.ws[f'L{self.row+1}'] = self.ws[f'L{self.row}'].value\
                .replace(str(self.row), str(self.row+1))
            self.ws[f'M{self.row+1}'] = self.ws[f'M{self.row}'].value\
                .replace(str(self.row), str(self.row+1))
            # copaimos los formatos de las celdas
            x = [
                'A', 'B', 'C',
                'D', 'E', 'F',
                'G', 'H', 'I',
                'J', 'K', 'L', 'M'
            ]
            for i in x:
                self.ws[f'{i}{self.row+1}']._style = self.ws[f'{i}{self.row}']._style
            # avanzamos a la siguiente fila
            self.row += 1

    def write_discounts(self): # Pasamos a los decsuentos
        if not len(self.bill['descuentos']) == 0:
            for item in self.bill['descuentos']:
                # insertamos la información
                self.ws[f'A{self.row}'] = self.row - 61
                self.ws[f'B{self.row}'] = item['code']
                self.ws[f'C{self.row}'] = 'Descuento'
                self.ws[f'D{self.row}'] = 'MP'  # No siempre
                self.ws[f'E{self.row}'] = item['val']
                self.ws[f'F{self.row}'] = 1
                self.ws[f'G{self.row}'] = item['val']
                self.ws[f'H{self.row}'] = 1
                self.ws[f'I{self.row}'] = item['val']
                self.ws[f'J{self.row}'] = item['iva']

                #Insertamos la siguiente fila:
                self.insert_new_row()
            
        # eliminamos la fila que sobra
        self.ws.delete_rows(self.row)

    def reorder(self):
        # ponemos en orden el desorden
        self.ws[f'F{self.row+2}'].value = str(self.ws[f'F{self.row+2}'].value)\
            .replace('F62', f'F{self.row-1}')
        self.ws[f'H{self.row+2}'].value = str(self.ws[f'H{self.row+2}'].value)\
            .replace('H62', f'H{self.row-1}')
        self.ws[f'I{self.row+2}'].value = str(self.ws[f'I{self.row+2}'].value)\
            .replace('I62', f'I{self.row-1}')
        self.ws[f'L{self.row+2}'].value = str(self.ws[f'L{self.row+2}'].value)\
            .replace('L62', f'L{self.row-1}')
        self.ws[f'M{self.row+2}'].value = str(self.ws[f'M{self.row+2}'].value)\
            .replace('M62', f'M{self.row-1}')

        # adecuamos las formaulas pertinentesa la infromacion que tenemos:
        r = 19
        I = [':$I$62', ':$K$62', ':$D$62']
        L = [':$L$62', ':$K$62', ':$D$62']
        M = [':$M$62', ':$K$62', ':$D$62']
        while r <= 46:
            for elem in I:
                self.ws[f'J{r}'].value = str(self.ws[f'J{r}'].value)\
                    .replace(elem, elem[:-2]+str(self.row))
            for elem in L:
                self.ws[f'L{r}'].value = str(self.ws[f'L{r}'].value)\
                    .replace(elem, elem[:-2]+str(self.row))
            for elem in M:
                self.ws[f'M{r}'].value = str(self.ws[f'M{r}'].value)\
                    .replace(elem, elem[:-2]+str(self.row))
            r += 1

    def overview(self):
        self.ws = self.wb['Resumen']
        bil = str()
        for elem in self.new.split('-'):
            if len(elem) != 2:
                bil = '0' + str(elem)
            bil += str(elem) + '-'
        bil = '\'' + bil[:-1] + '\''
        self.row = 60
        # buscamos el grupo de celdas con el que trabajar:
        while not str(self.ws[f'B{self.row}'].value).startswith('=Sig'):
            self.row += 1
        # iteramos las columnas y modificamos lo que hay que modificar:
        for i in range(2):
            col = 1
            while self.ws.cell(row=self.row, column=col).value is not None:
                # modifiquemos lo pertinente:
                if str(self.ws.cell(row=self.row+i, column=col).value).startswith('=Sig'):
                    self.ws.cell(row=self.row+i, column=col).value = str(
                        self.ws.cell(row=self.row+i, column=col).value)\
                        .replace('Siguiente', bil)
                col += 1


if __name__ == '__main__':
    xcel = 'C:/Users/osgum/Desktop/Zotz/2021-Gastos MAKRO.xlsx'
    pdf = '///Users/osgum/Desktop/Zotz/Facturas_MAKRO/21-01-08-MAKRO-02.pdf'
    test = Excel(xcel, pdf)
    print('Done!')

# __NOTES__ #
'''


'''

# __BIBLIOGRAPHY__ #
'''
    pypi:       https: // pypi.org/project/openpyxl/
    openpyxl:   https: // openpyxl.readthedocs.io/en/stable/
'''
