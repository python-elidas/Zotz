'''
Author: Elidas              |   Python Version: 3.9.9
Date: 2/7/2024, 12:39:50    |   version: 0.0.1
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
class Merkadona:
    def __init__(self, file_path='C:/Users/Elidas/github/Zotz/files/Extras/2022/MAKRO/22-01-10 - MAKRO - 0-0(014)0010-(2022)010015.pdf'):
        __reader = PdfReader(file_path)
        # Obtenemos el nombre de la factura para plasmarlo en el Excel
        self.__file_name = file_path.split(
            '/')[-1].split('.')[0].split(' - ')[-1]
        # creamos el diccionario que se va a devolver
        self.__factura = dict()
        self.__pages = __reader.pages
        self.__get_text_as_list()
        self.__clean_info()
        self.__get_bill_date()
        self.__get_bill_number()
        self.__get_items()
        self.__get_discount()
        self.__get_total()

    def __get_text_as_list(self):
        self.__info = [page.extract_text().split('\n')
                       for page in self.__pages]

    def __clean_info(self):
        clean = list()
        for page in self.__info:
            for row in page:
                clean.append(' '.join(row.split()))  # ? Nota 1
        self.__info = clean

    def __get_bill_date(self):
        pass

    def __get_bill_number(self):
        pass
        
    def __get_items(self):
        pass
    
    def __get_discount(self):
        pass
    
    def __get_total(self):
        pass

    def export_info(self):
        with open('merkadona_info.txt', 'w') as fw:
            for row in self.__info:
                fw.write(row + '\n')

    def print_factura(self):
        print(self.__factura)

    def get_resultados(self):
        # Getter de los resultados
        return self.__file_name, self.__factura


# __Main Run__#
if __name__ == '__main__':
    item = Merkadona()
    # item.write_info()
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
