'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9
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
        content = parser.from_file(file_path)  # Ruta completa
        meta, raw = content['metadata'], content['content']
        pages = list(meta.keys())[-1]
        raw = raw.replace('\n\n', '\n').split('\n')
        self.clean(raw)
        # creamos el diccionario que devolveremos al final
        self.factura = dict()
        # obtenemos la fecha de la factura:
        self.get_date()
        # Obtenemos el numero de factura:
        self.get_bill_num()
        
        for i in range(int(meta[pages])):
            #print(f'[*] vuelta: {i}')
            #if i >= 1:
            #    [print(f'row: {i}') for i in self.safe_text]
            # Limpiamos nuevamente:
            self.clean2()
            #[print(f'row: {i}') for i in self.safe_text if not len(i) == 1]
            # Obtenemos los articulos:
            try:
                self.get_items()
            except Exception:
                try:
                    self.get_items_v2()
                except:
                    break
            
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
        # print('[-] clean')
        if '**FACTURA IVA**' in raw:
            n = raw.index('**FACTURA IVA**') + 1
        elif 'DATOS FISCALES' in raw:
            n = raw.index('DATOS FISCALES') + 1
        self.safe_text = raw[n:]

    def get_date(self):
        # print('[-] get_date')
        for row in self.safe_text:
            if row.startswith('FECHA') or row.startswith('Fecha'):
                self.factura['fecha'] = row.split(':')[-1].strip()
                break

    def get_bill_num(self):
        # print('[-] get_bill_num')
        self.factura['Factura'] = list()
        for row in self.safe_text:
            if row.startswith('NUM. FACTURA') or \
            row.startswith('FACTURA SIMPLIFICADA') or \
            row.startswith('Factura Simplificada'):
                self.factura['Factura'].append(row.split(':')[-1].strip())
            elif row.startswith('Nº Factura'):
                n = row.split('Fecha')[0].split(':')[-1].strip()
                self.factura['Factura'].append(n)
                
            if len(self.factura['Factura']) == 2:
                break
                
    def clean2(self):  # Limpiamos las siguientes líneas)
        # print('[-] clean2')
        n = 0
        for row in self.safe_text:
            if 'LINEA' in row:
                break
            elif 'Descripción' in row:
                break
            elif 'TARJETA BANCARIA' in row:
                break
            elif 'TIPO' in row:
                break
            else:
                #print(f'row: {row}; {n}')
                n += 1
        self.safe_text = self.safe_text[n+1:]
        
    def get_items(self):
        # print('[-] get_items')
        n = 0
        # creamos in diccionario con los ids de los ivas:
        iva = {'10': 1, '21': 2, '4': 5, '0': 6}
        # creamos la lista que almacenará los articulos
        if not 'articulos' in self.factura:
            # creamos la lista que almacenará los articulos
            self.factura['articulos'] = list()
        # Creamos la lista de descuentos por si existen descuentos inline
        # self.factura['descuentos'] = list() # !Nota 2
        # creamos la lista con los códigos de los descuentos
        for row in self.safe_text:
            # print(f'[*] row: {row}')
            D = dict()  # Los articulos se almacenan en forma de diccionario
            if 'TIPO' not in row and 'Total Factura' not in row and not row == '':
                n += 1
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
                #print(f'{row}\nlen: {len(row)}')
                info = row.split()
                D['codigo'] = self.gen_code(' '.join(info[2:-3]))  #! Nota 1
                D['desc'] = ' '.join(info[2:-3])
                D['prec ud'] = float(info[-3].replace(',', '.'))
                D['ud pac'] = float(1)
                D['precio'] = float(info[-1].replace(',', '.'))
                D['uds'] = int(info[1])
                D['iva'] = int(iva[info[-2][:-1]])
                self.factura['articulos'].append(D)                    
            else:
                break
        self.safe_text = self.safe_text[n:]
    
    def gen_code(self, string):
        if string.startswith('PARK'):
            string = 'PARKING'
        model = hash.new('sha256')
        model.update(string.encode('utf-8'))
        return model.hexdigest()[:10]

    def get_items_v2(self):
        # print('[-] get_items_v2')
        n = 0
        # creamos in diccionario con los ids de los ivas:
        iva = {'10': 1, '21': 2, '4': 5, '0': 6}
        if not 'articulos' in self.factura:
            # creamos la lista que almacenará los articulos
            self.factura['articulos'] = list()
            # Creamos la lista de descuentos por si existen descuentos inline
            # self.factura['descuentos'] = list() # !Nota 2
        # creamos la lista con los códigos de los descuentos
        for row in self.safe_text:
            D = dict()  # Los articulos se almacenan en forma de diccionario
            n += 1
            if not row.startswith('TOTAL'):
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
                if not len(row) == 0:
                    info = row.split()
                    #print(f'{info}\nlen: {len(info)}')
                    D['codigo'] = self.gen_code(' '.join(info[:-6]))  #! Nota 1
                    D['desc'] = ' '.join(info[:-6])
                    D['prec ud'] = float(info[-5].replace(',', '.'))
                    D['ud pac'] = float(1)
                    D['precio'] = float(info[-4].replace(',', '.'))
                    D['uds'] = int(info[-6])
                    D['iva'] = int(iva[info[-3][:-1]])
                    self.factura['articulos'].append(D)                    
            else:
                self.safe_text = self.safe_text[n:]
                break
            
    def get_disc(self):
       pass

    def get_ammont(self):
        for row in self.safe_text:
            #print(f'[*] get_ammont: {row}')
            if 'Total Factura' in row:
                self.factura['total'] = row.split(' ')[-1][:-1]
            elif 'TOTAL FACTURA' in row:
                self.factura['total'] = row.split(' ')[-2]

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


def run(files, txt=False, verbose=True):
    import os
    dir = 'C:/Users/osgum/Desktop/Ztotz/Facturas_MERCADONA'
    if len(files) == 0:
        #dir += '/test'
        files = os.listdir(dir)
    for file in files:
        if '.pdf' in file:
            pdf = f"{dir.replace('C:/', '///')}/{file}"
            print(f'Item: {file}')
            try:
                M = Mercadona(pdf)
                name, factura = M.result()
                if verbose:
                    my_print(factura)
                if txt:
                    txt = dir + '/txt/' + file.replace('.pdf', '.txt')
                    to_txt(txt, factura)
            except PermissionError:
                pass


if __name__ == '__main__':
    file = ['21-02-19 - Mercadona - A-V2021-00000469390.pdf',]
    #file = ['21-12-16 - Mercadona - A-V2021-00004340365.pdf',]
    #file = list()
    run(file, txt=True, verbose=True)

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