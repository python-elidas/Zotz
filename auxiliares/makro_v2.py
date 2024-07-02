'''
Author: Elidas              |   Python Version: 3.9.9
Date: 11/6/2024, 12:39:50   |   version: 0.0.1
'''

# __LIBRARIES__ #
from pypdf import PdfReader
if __name__ == '__main__':
    from functionals import clean_row
    from toolPrint import dictPrint
else:
    from auxiliares.functionals import clean_row
    from auxiliares.toolPrint import dictPrint

# __AUXILIARY__#


# __MAIN CODE__ #
class Makro:
    def __init__(self, file_path):
        __reader = PdfReader(file_path)
        # Obtenemos el nombre de la factura para plasmarlo en el Excel
        self.__file_name = file_path.split(
            '/')[-1].split('.')[0].split(' - ')[-1]
        # creamos el diccionario que se va a devolver
        self.__factura = dict()
        self.__pages = __reader.pages
        self.__get_text_as_list()
        self.__get_bill_date()
        self.__get_bill_number()
        self.__get_items()
        self.__get_discount()
        self.__get_total()

    def __get_text_as_list(self):
        self.__info = list()
        pages = [page.extract_text().split('\n')
                 for page in self.__pages]
        [self.__info.append(row) for page in pages for row in page]
        #!print(self.__info)

    def __clean_row(self, row):
        return ' '.join(row.split())

    def __format_item_row(self, row):
        return [i.strip().replace(',', '.') for i in row.split('  ') if not i == '' or i == 'M']

    def __get_bill_date(self):
        for row in self.__info:
            if 'Fecha de venta' in row:
                self.__factura['fecha'] = self.__clean_row(row).split(
                    'Fecha de venta: ')[-1].split()[0]
                self._info = self.__info[self.__info.index(row):]

    def __get_bill_number(self):
        for row in self.__info:
            if 'Factura' in row:
                bill_number = self.__clean_row(row).split(' ')[
                    1].replace('/', '-')
                self._info = self.__info[self.__info.index(row):]
                break
        self.__factura['Factura'] = bill_number

    def __get_items(self):
        n, items = 0, list()
        conceptos = ['codigo', 'desc', 'N/A', 'prec ud',
                     'ud pac', 'precio', 'uds', 'N/A', 'iva']
        for row in self.__info:
            if row.startswith('-') and row.endswith('-'):
                n += 1
            if n == 3 and not (row.startswith('-') and row.endswith('-')):
                f_row, item = self.__format_item_row(row), dict()
                for info in f_row:
                    index = f_row.index(info)
                    try:
                        if not conceptos[index] == 'N/A':
                            # print(conceptos[index])
                            item[conceptos[index]] = info
                    except IndexError:
                        pass
                items.append(item)
                self._info = self.__info[self.__info.index(row):]
            if n == 4:
                break
        self.__factura['articulos'] = items

    def __get_discount(self):
        pass

    def __get_total(self):
        for row in self.__info:
            if 'Total a pagar' in row:
                self.__factura['total'] = self.__clean_row(
                    row).split('Total a pagar')[-1].replace(',', '.').strip()

    def export_info(self):
        with open('makro_info.txt', 'w') as fw:
            for row in self.__info:
                fw.write(' '.join(row.split()) + '\n')  # ? Nota 1

    def print_factura(self):
        print(self.__factura)

    def get_resultados(self):
        # Detter de los resultados
        return self.__file_name, self.__factura


# __Main Run__#
if __name__ == '__main__':
    item = Makro('C:/Users/Elidas/github/Zotz/files/Extras/2022/MAKRO/22-01-10 - MAKRO - 0-0(014)0010-(2022)010015.pdf')
    item.export_info()
    item.print_factura()

# __NOTES__ #
'''
self.factura = {
    fecha:      'fecha de la factura'   (str),
    Factura:    'Numero de la factura'  (str),
    articulos: [ <-- lista de items
        {
            codigo:     código del articulo         (str),
            desc:       descripción del articulo    (str),
            prec ud:    precio unitario             (float),
            ud pac:     unidades por paquete        (float),
            precio:     precio total                (float),
            uds:        Unidades del producto       (int),
            iva:        código del iva              (int) 
        }, <-- uno por item
    ],
    descuentos: [ <-- lista de descuentos
        {
            code:   código del descuento    (str),
            val:    valor del descuento     (float),
            iva:    código del iva          (int)
        }, <-- uno por descuento
    ]
}

Nota 1:
    la estructura ' '.join(string.split()) ha sido hallada en stackoverflow
    (como no) y su función viene a ser la de eliminar los espacios en blanco
    innecesarios en la cadena que se ponga como 'string'
'''

# __BIBLIOGRAPHY__ #
'''
    stackoverflow:  https://stackoverflow.com/
'''
