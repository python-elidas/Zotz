'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-26T11:18:58.589Z
Version: 0.0.1
'''

# __LYBRARIES__ #
import openpyxl as xls
import simply_sqlite as SQL
from makro import Makro
from datetime import datetime

# __MAIN CODE__ #


class Excel:
    def __init__(self, xcel, pdf):
        # obtiene la fecha de hoy
        self.today = datetime.now().strftime('%x')
        # accedemos a la base de datos
        self.db = SQL.SQL('files/zotz_db')
        # accedemos al excel
        self.wb = xls.load_workbook(filename=xcel, read_only=False)
        # obtenemos el nombre de la factura y su información
        M = Makro(pdf)
        self.new, self.bill = M.result()  # generalizar
        # ejecutamos el codigo de la Factura
        self.write_bill()
        # ejecutamos el siguiente paso:
        self.overview()
        # Guardamos los cambios
        self.wb.save(xcel)

    def write_bill(self):
        # creamos la hoja con la que trabajaremos
        ws = self.wb.copy_worksheet(self.wb['Siguiente'])
        # Establecemos el tituo de la nueva hoja
        ws.title = self.new
        # COMENZAMOS A INTRODUCIR INFORMACIÓN
        # número de factura y fecha
        ws['G2'] = self.bill['Factura'][0]
        ws['G3'] = self.bill['Factura'][1]
        ws['G4'] = self.bill['fecha']

        # empezamos con los articulos:
        items = self.bill['articulos']
        row = 62
        for item in items:
            ws[f'A{row}'] = row - 61  # escribimos el numero de la fila
            ws[f'B{row}'] = item['codigo']  # escribimos la referencia
            ws[f'C{row}'] = item['desc']  # escribimos la descripción
            # obtenemos la referencia del tipo de producto
            if len(self.db.show_one_row(
                'Articulos', 'Codigo', item['codigo']
            )) == 0:
                # Main_Frame.new_item(item)
                ws[f'D{row}'] = 'PNDT'
            else:
                ws[f'D{row}'] = self.db.show_one_row(
                    'Articulos', 'Codigo', item['codigo'])[0][2]
            ws[f'E{row}'] = item['prec ud']
            ws[f'F{row}'] = item['ud pac']
            ws[f'G{row}'] = item['precio']
            ws[f'H{row}'] = item['uds']
            ws[f'I{row}'] = item['precio'] * int(item['uds'])
            ws[f'J{row}'] = item['iva']

            # insertamos la siguiente fila
            ws.insert_rows(row+1)
            # cpiamos las formulas pertinentes
            ws[f'K{row+1}'] = str(ws[f'K{row}'].value)\
                .replace(str(row), str(row+1))
            ws[f'L{row+1}'] = ws[f'L{row}'].value\
                .replace(str(row), str(row+1))
            ws[f'M{row+1}'] = ws[f'M{row}'].value\
                .replace(str(row), str(row+1))
            # copaimos los formatos de las celdas
            x = [
                'A', 'B', 'C',
                'D', 'E', 'F',
                'G', 'H', 'I',
                'J', 'K', 'L', 'M'
            ]
            for i in x:
                ws[f'{i}{row+1}']._style = ws[f'{i}{row}']._style
            # avanzamos a la siguiente fila
            row += 1

        # Pasamos a los decsuentos
        if len(self.bill['descuentos']) != 0:
            for item in self.bill['descuentos']:
                # insertamos la información
                ws[f'A{row}'] = row - 61
                ws[f'B{row}'] = item['code']
                ws[f'C{row}'] = 'Descuento'
                ws[f'D{row}'] = 'MP'  # No siempre
                ws[f'E{row}'] = item['val']
                ws[f'F{row}'] = 1
                ws[f'G{row}'] = item['val']
                ws[f'H{row}'] = 1
                ws[f'I{row}'] = item['val']
                ws[f'J{row}'] = item['iva']

                # insertamos la siguiente fila
                ws.insert_rows(row+1)
                # cpiamos las formulas pertinentes
                ws[f'K{row+1}'] = str(ws[f'K{row}'].value)\
                    .replace(str(row), str(row+1))
                ws[f'L{row+1}'] = ws[f'L{row}'].value\
                    .replace(str(row), str(row+1))
                ws[f'M{row+1}'] = ws[f'M{row}'].value\
                    .replace(str(row), str(row+1))
                # copaimos los formatos de las celdas
                x = [
                    'A', 'B', 'C',
                    'D', 'E', 'F',
                    'G', 'H', 'I',
                    'J', 'K', 'L', 'M'
                ]
                for i in x:
                    ws[f'{i}{row+1}']._style = ws[f'{i}{row}']._style
                # avanzamos a la siguiente fila
                row += 1

        # eliminamos la fila que sobra
        ws.delete_rows(row)

        # ponemos en orden el desorden
        ws[f'F{row+2}'].value = str(ws[f'F{row+2}'].value)\
            .replace('F62', f'F{row-1}')
        ws[f'H{row+2}'].value = str(ws[f'H{row+2}'].value)\
            .replace('H62', f'H{row-1}')
        ws[f'I{row+2}'].value = str(ws[f'I{row+2}'].value)\
            .replace('I62', f'I{row-1}')
        ws[f'L{row+2}'].value = str(ws[f'L{row+2}'].value)\
            .replace('L62', f'L{row-1}')
        ws[f'M{row+2}'].value = str(ws[f'M{row+2}'].value)\
            .replace('M62', f'M{row-1}')

        # adecuamos las formaulas pertinentesa la infromacion que tenemos:
        r = 19
        I = [':$I$62', ':$K$62', ':$D$62']
        L = [':$L$62', ':$K$62', ':$D$62']
        M = [':$M$62', ':$K$62', ':$D$62']
        while r <= 46:
            for elem in I:
                ws[f'J{r}'].value = str(ws[f'J{r}'].value)\
                    .replace(elem, elem[:-2]+str(row))
            for elem in L:
                ws[f'L{r}'].value = str(ws[f'L{r}'].value)\
                    .replace(elem, elem[:-2]+str(row))
            for elem in M:
                ws[f'M{r}'].value = str(ws[f'M{r}'].value)\
                    .replace(elem, elem[:-2]+str(row))
            r += 1

    def overview(self):
        ws = self.wb['Resumen']
        bil = str()
        for elem in self.new.split('-'):
            if len(elem) != 2:
                bil = '0' + str(elem)
            bil += str(elem) + '-'
        bil = '\'' + bil[:-1] + '\''
        row = 60
        # buscamos el grupo de celdas con el que trabajar:
        while not str(ws[f'B{row}'].value).startswith('=Sig'):
            row += 1
        # iteramos las columnas y modificamos lo que hay que modificar:
        for i in range(2):
            col = 1
            while ws.cell(row=row, column=col).value is not None:
                # modifiquemos lo pertinente:
                if str(ws.cell(row=row+i, column=col).value).startswith('=Sig'):
                    ws.cell(row=row+i, column=col).value = str(
                        ws.cell(row=row+i, column=col).value)\
                        .replace('Siguiente', bil)
                col += 1


if __name__ == '__main__':
    xcel = 'C:/Users/osgum/Desktop/Zotz/2021-Gastos MAKRO.xlsx'
    pdf = '///Users/osgum/Desktop/Zotz/Facturas_MAKRO/21-05-08-MAKRO-01.pdf'
    test = Excel(xcel, pdf)

# __NOTES__ #
'''


'''

# __BIBLIOGRAPHY__ #
'''
    pypi:       https: // pypi.org/project/openpyxl/
    openpyxl:   https: // openpyxl.readthedocs.io/en/stable/
'''
