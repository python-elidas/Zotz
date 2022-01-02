'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-24
Version: 1.0.0
'''

# __LYBRARIES__ #
from tika import parser
from tkinter import messagebox
import simply_sqlite as SQL
import hashlib as hash


# __MAIN CODE__ #
class Mercadona:
    def __init__(self, file_path):
        # Nos quedamos solo con el nombre del archivo.
        file_name = file_path.split('/')[-1].split('.')[0]
        # Cogemos el nombre de la hoja 
        self.file = file_name.split(' - ')[-1]
        if '.pdf' in self.file:
            self.file = self.file.replace('.pdf', '')
        print(f'File {self.file} loaded.')
        # __lectura del archivo__ #
        raw = parser.from_file(file_path)  # Ruta completa
        self.clean(raw)
        # creamos el diccionario que devolveremos al final
        self.factura = dict()
        # obtenemos la fecha de la factura:
        self.get_date()
        # Obtenemos el numero de factura:
        self.get_bill_num()
        # Limpiamos nuevamente:
        self.clean2()
        # Obtenemos los articulos:
        self.get_items()
        # si no es devolucion
        
        # Obtenemos el total de la factura:
        self.get_ammont()
        print(f'File {self.file} readed.')
        
    def print_info(self, raw):
        for key in list(raw.keys()):
            if type(raw[key]) is dict:
                print(list(raw[key].keys()))
                self.print_info(raw[key])
            else:
                print(f'{key}: {raw[key]}')
                return True

    def clean(self, raw):
        n = 0
        for item in raw['content'].replace('\n\n', '\n').split('\n'):
            if not item.startswith('**FACTURA IVA**'):
                n+=1
            else:
                break
        self.safe_text = raw['content']\
                        .replace('\n\n', '\n').split('\n')[n:]

    def get_date(self):
        for row in self.safe_text:
            if row.startswith('FECHA'):
                self.factura['fecha'] = row.split(':')[-1].replace(' ', '')
                break

    def get_bill_num(self):
        self.factura['Factura'] = list()
        for row in self.safe_text:
            if row.startswith('NUM. FACTURA') or \
            row.startswith('FACTURA SIMPLIFICADA'):
                self.factura['Factura'].append(row.split(':')[-1].replace(' ', ''))
                if len(self.factura['Factura']) == 2:
                    break
                
    def clean2(self):  # Limpiamos las siguientes líneas
        n = 1
        for row in self.safe_text:
            if not row.startswith('LINEA'):
                n += 1
            else:
                self.safe_text = self.safe_text[n:]
                break
            
    def get_items(self):
        n = 0
        # creamos in diccionario con los ids de los ivas:
        iva = {'10': 1, '21': 2, '4': 5, '0': 6}
        # creamos la lista que almacenará los articulos
        self.factura['articulos'] = list()
        # Creamos la lista de descuentos por si existen descuentos inline
        # self.factura['descuentos'] = list() # !Nota 2
        # creamos la lista con los códigos de los descuentos
        for row in self.safe_text:
            D = dict()  # Los articulos se almacenan en forma de diccionario
            n += 1
            if not row.startswith('TIPO'):
                # eliminamos los caracteres extraños
                row = row\
                    .replace('\\xc2\\x9c', 'U')\
                    .replace('\\xc2\\xb1', '~')\
                    .replace('\\xc2\\xb4', ' ')\
                    .replace('\\xc2\\xba', '.')\
                    .replace('\\xe2\\x82\\xac', 'E')\
                    .replace('\\xc3\\x81', 'A')\
                    .replace('\\xc3\\x89', 'E')\
                    .replace('\\xc3\\x8d', 'I')\
                    .replace('\\xc3\\x91', 'N')\
                    .replace('\\xc3\\x93', 'O')\
                    .replace('\\xc3\\x9a', 'U')\
                    .replace('\'', ' ')\
                # solo se tienen en cuenta las filas con información relevante
                # print(f'{row}\nlen: {len(row)}')
                info = row.split()
                D['codigo'] = self.gen_code(' '.join(info[2:-3]))  #! Nota 1
                D['desc'] = ' '.join(info[2:-3])
                D['prec ud'] = float(info[-3].replace(',', '.'))
                D['ud pac'] = float(1)
                D['precio'] = float(info[-3].replace(',', '.'))
                D['uds'] = int(info[1])
                D['iva'] = int(iva[info[-2][:-1]])
                self.factura['articulos'].append(D)                    
            else:
                self.safe_text = self.safe_text[n:]
                break
    
    def gen_code(self, string):
        model = hash.new('sha256')
        model.update(string.encode('utf-8'))
        return model.hexdigest()[:10]

    def get_items_v2(self):
        pass
            
    def get_disc(self):
       pass

    def get_ammont(self):
        for row in self.safe_text:
            if row.startswith('TOTAL'):
                self.factura['total'] = row.split()[-2]

    def result(self):
        return self.file, self.factura


def my_print(d):
    for key in d.keys():
        print(f'{key}\n')
        if type(d[key]) is list:
            for item in d[key]:
                print(f'\t{item}')
        else:
            print(f'\t{d[key]}')


def to_txt(txt, factura):
    info = open(txt, 'w')
    for item in factura:
        if type(factura[item]) != list:
            info.write(f'{item} : {factura[item]}\n')
        else:
            info.write(f'{item}\n')
            for articulo in factura[item]:
                info.write(f'\t{articulo}\n')
    info.close()


def run(files):
    import os as file
    dir = 'C:/Users/osgum/Desktop/Zotz/Facturas_MERCADONA'
    for item in files:
        print(f'Item: {item}')
        try:
            pdf = dir.replace('C:', '//') + '/' + item
            # txt = dir + '/txt/' + item.replace('.pdf', '.txt')
            M = Mercadona(pdf)
            name, factura = M.result()
            my_print(factura)
            # to_txt(txt, factura)
        except PermissionError:
            pass


if __name__ == '__main__':
    files = ['21-01-08 - Mercadona - A-V2021-55203.pdf']
    # files = file.listdir(dir)
    run(files)

# __NOTES__ #
'''
Nota 1:
    la estructura ' '.join(string.split()) ha sido hallada en stackoverflow
    (como no) y su funcion viene a ser la de eliminar los espacios en blanco
    innecesarios en la cadena que se ponga como 'string'
    
Nota 2:
    Mercadona parece no tener descuentos por los que no ha de tenerse en cuenta, 
    en caso de aparecer en algún momento habrá que implementarlos.
'''
# __BIBLIOGRAPHY__ #
'''
    W3Schools:      https://www.w3schools.com/python/python_reference.asp
    stackoverflow:  https://stackoverflow.com/
'''
