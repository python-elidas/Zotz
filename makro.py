'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9
Date: 2021-08-24
Version: 2.0.0
'''

# __LYBRARIES__ #
from tika import parser
from tkinter import messagebox
from auxiliares.toolPrint import dictPrint


# __MAIN CODE__ #
class Makro:
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
        pages = int(raw['metadata'][list(raw['metadata'].keys())[-1]])
        #[print(i) for i in raw['content'].split('\n')]
        # self.print_info(raw)
        raw = str(raw['content'])  # Seleccionamos el contenido relevante
        #print(raw)
        # establecemos codificación
        safe_text = raw.encode('utf-8', errors='ignore')
        # separamos de forma que sea cómodo
        self.safe_text = str(safe_text).split('\\n')
        # quitamos la morralla
        self.clean()
        # creamos el diccionario que devolveremos al final
        self.factura = dict()
        # obtenemos la fecha de la factura:
        self.get_date()
        # Obtenemos el numero de factura:
        self.get_bill_num()
        # Quitamos mas morralla
        self.clean2()
        for i in range(pages):
            if i > 0:
                self.clean3()            
            # Obtenemos los articulos:
            try:
                self.get_items()
            except ValueError:
                self.get_items_v2()
            # si no es devolucion
            if not 'Factura devolucion' in list(self.factura.keys()):
                # verificamos la existencia de descuentos 
                try:
                    self.get_disc()
                except Exception:
                    self.get_disc_v2()
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

    def clean(self):
        # buscamos donde empiea lo interesante
        n = 0
        for row in self.safe_text:
            if not row.startswith('MAKRO AUTOSERVICIO MAYORISTA'):
                n += 1
            else:
                break
        # nos quedamos solo con lo que interesa
        self.safe_text = self.safe_text[n:]

    def get_date(self):
        n = 0
        for row in self.safe_text:
            n += 1
            # Obtenemos la fecha de la factura
            if not row.find('Fecha de venta:') == -1:
                fecha = list()
                for item in row.split(' '):
                    if item != '':
                        fecha.append(item)
                self.factura['fecha'] = fecha[-2]
                self.safe_text = self.safe_text[n:]
                break

    def get_bill_num(self):
        n = 0
        bool = False
        for row in self.safe_text:
            n += 1
            if bool and not row.find('factura') == -1:
                row = row.split('  ')
                while row.count('') != 0:
                    row.remove('')
                self.factura[row[0][:-15]] = row[1].split(' ')[1].replace('/', '-')
                self.safe_text = self.safe_text[n:]
                break
            if not bool and not row.find('Factura') == -1:
                row = row.split('  ')
                while row.count('') != 0:
                    row.remove('')
                self.factura[row[0]] = row[1:3]
                self.factura[row[0]][0] = self.factura[row[0]][0]\
                    .replace('/', '-').replace(' ', '')
                # comprobamos que no es una devolución
                if row[0].startswith('Factura d'):
                    bool = True
                if not bool:
                    self.safe_text = self.safe_text[n:]
                    break

    def clean2(self):  # Limpiamos las siguientes líneas
        n = 0
        sep = 0
        for row in self.safe_text:
            n += 1
            if row.startswith('-'):
                sep += 1
            if sep == 3:
                self.safe_text = self.safe_text[n:]
                break
    
    def clean3(self):
        n = 0
        for row in self.safe_text:
            n += 1
            if row.strip().startswith('Total de'):
                self.safe_text = self.safe_text[n:]
                break

    def get_items(self):
        n = 0
        if not 'articulos' in self.factura:
            # creamos la lista que almacenará los articulos
            self.factura['articulos'] = list()
            # Creamos la lista de descuentos por si existen descuentos inline
            self.factura['descuentos'] = list()
        # creamos la lista con los códigos de los descuentos
        self.desc = list()
        for row in self.safe_text:
            D = dict()  # Los articulos se almacenan en forma de diccionario
            n += 1
            if not row.startswith('-') and not row.startswith('N\\xc3\\xbamero'):
                # eliminamos los carácteres extraños
                row = row\
                    .replace('\\xc2\\xaa', 'a')\
                    .replace('\\xc3\\xba', 'u')\
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
                    .replace('\\xc2\\x9c', 'U')\
                    .replace('\'', ' ')\
                # solo se tienen en cuenta las filas con infromacion relevante
                # print(f'{row}, n = {n}\n')
                if len(row) > 100 and not '-' in row[80:90]:
                    D['codigo'] = ' '.join(row[3:18].split())  #! Nota 1
                    D['desc'] = ' '.join(row[18:52].split())
                    D['prec ud'] = float(' '.join(row[57:70]
                                                .replace(',', '.').split()))
                    D['ud pac'] = float(' '.join(row[70:80]
                                                .replace(',', '.').split()))
                    D['precio'] = float(' '.join(row[80:90]
                                                .replace(',', '.').split()))
                    if '-' in row[90:99]:
                        D['uds'] = int(' '.join(row[90:99].split())\
                            .replace('-', '')) * -1
                    else:
                        D['uds'] = int(' '.join(row[90:99].split()))
                    iva = int(' '.join(row[108:112].split()))
                    if iva == 0:
                        iva = 6
                    D['iva'] = iva
                    self.factura['articulos'].append(D)
                    d_cod = ' '.join(row[118:126].split()) 
                    if not d_cod == '' and len(d_cod) > 1:
                        self.desc.append(row[118:126])
                        #print('v1')
                elif len(row) > 100 and '-' in row[80:90]:
                    D['code'] = ' '.join(row[3:18].split())
                    D['val'] = float(' '.join(row[80:90]
                                            .replace(',', '.').split())\
                                                .replace('-', '')) * -1
                    D['iva'] = int(' '.join(row[108:112].split()))
                    self.factura['descuentos'].append(D)
            else:
                self.safe_text = self.safe_text[n:]
                break

    def get_items_v2(self):
        n = 0
        if not 'articulos' in self.factura:
            # creamos la lista que almacenará los articulos
            self.factura['articulos'] = list()
            # Creamos la lista de descuentos por si existen descuentos inline
            self.factura['descuentos'] = list()
        # creamos la lista con los códigos de los descuentos
        self.desc = list()
        for row in self.safe_text:
            D = dict()  # Los articulos se almacenan en forma de diccionario
            n += 1
            if not row.startswith('-') and not row.startswith('N\\xc3\\xbamero'):
                # eliminamos los carácteres extraños
                row = row\
                    .replace('\\xc2\\xaa', 'a')\
                    .replace('\\xc3\\xba', 'u')\
                    .replace('\\xc2\\xb1', '~')\
                    .replace('\\xc2\\xb4', ' ')\
                    .replace('\\xc2\\xba', '.')\
                    .replace('\\xc3\\x81', 'A')\
                    .replace('\\xc3\\x89', 'E')\
                    .replace('\\xc3\\x8d', 'I')\
                    .replace('\\xc3\\x91', 'N')\
                    .replace('\\xc3\\x93', 'O')\
                    .replace('\\xc3\\x9a', 'U')\
                    .replace('\\xc2\\x9c', 'U')\
                    .replace('\'', ' ')\
                # solo se tienen en cuenta las filas con infromacion relevante
                row = [item.strip() for item in row.split('   ') if not item == '' and not item == 'M']
                print(f'{row}')
                if len(row) >= 9 and not '-' in str(row[5]):
                    D['codigo'] = row[0]
                    D['desc'] = row[1]
                    D['prec ud'] = float(str(row[3]).replace(',', '.'))
                    D['ud pac'] = float(str(row[4]).replace(',', '.'))
                    D['precio'] = float(str(row[5]).replace(',', '.'))
                    if '-' in str(row[6]):
                        D['uds'] = int(str(row[6]).replace('-', '')) * -1
                    else:
                        D['uds'] = int(row[6])
                    D['iva'] =int(row[8])
                    self.factura['articulos'].append(D)
                    #print(row)
                    if len(row) > 9 and len(row[9].strip()) > 1:
                        self.desc.append(row[8:])
                        #print('v2')
                elif len(row) >= 9 and '-' in str(row[5]):
                    D['code'] = row[0]
                    D['val'] = float(str(row[5])
                                            .replace(',', '.')\
                                            .replace('-', '')) * -1
                    D['iva'] = int(row[8])
                    self.factura['descuentos'].append(D)  
            else:
                self.safe_text = self.safe_text[n:]
                break
            
    def get_disc(self):
        n = 0
        if len(self.factura['descuentos']) == 0:
            self.factura['descuentos'] = list()
        for row in self.safe_text:
            row = row\
                        .replace('\\xc2\\x9c', 'U')\
                        .replace('\\xc2\\xaa', 'a')\
                        .replace('\\xc2\\xb1', '~')\
                        .replace('\\xc2\\xb4', ' ')\
                        .replace('\\xc2\\xba', '.')\
                        .replace('\\xc3\\x81', 'A')\
                        .replace('\\xc3\\x89', 'E')\
                        .replace('\\xc3\\x8d', 'I')\
                        .replace('\\xc3\\x91', 'N')\
                        .replace('\\xc3\\x93', 'O')\
                        .replace('\\xc3\\x9a', 'U')\
                        .replace('\'', ' ')
            #print(self.desc)
            if self.desc and not row.startswith('-'):
                row = ' '.join(row.split()).split()
                #print(row)
                D = dict()
                D['val'] = float(row[-3][:-1].replace(',', '.')) * -1
                D['iva'] = int(row[-2])
                D['code'] = row[-1]
                self.factura['descuentos'].append(D)
                n += 1
            elif row.startswith('-') and n >= 1:
                self.safe_text = self.safe_text[n:]
                break
    
    def get_disc_v2(self):
        n = 0
        if len(self.factura['descuentos']) == 0:
            self.factura['descuentos'] = list()
        for row in self.safe_text:
            row = row\
                        .replace('\\xc2\\xaa', 'a')\
                        .replace('\\xc2\\xb1', '~')\
                        .replace('\\xc2\\xb4', ' ')\
                        .replace('\\xc2\\xba', '.')\
                        .replace('\\xc3\\x81', 'A')\
                        .replace('\\xc3\\x89', 'E')\
                        .replace('\\xc3\\x8d', 'I')\
                        .replace('\\xc3\\x91', 'N')\
                        .replace('\\xc3\\x93', 'O')\
                        .replace('\\xc3\\x9a', 'U')\
                        .replace('\\xc2\\x9c', 'U')\
                        .replace('\'', ' ')
            if self.desc and not row.startswith('-'):
                row = [i.strip() for i in row.split('   ') if not i == '']
                #print(row)
                if not len(row) == 0:
                    D = dict()
                    D['val'] = float(row[-3][:-1].replace(',', '.')) * -1
                    D['iva'] = int(row[-2])
                    D['code'] = row[-1]
                    self.factura['descuentos'].append(D)
                n += 1
            elif row.startswith('-') and n >= 1:
                self.safe_text = self.safe_text[n:]
                break

    def get_ammont(self):
        for row in self.safe_text:
            if not row.find('Total a pagar') == -1:
                if '-' in row:
                    self.factura['total'] = ' '.join(row.split())\
                        .split()[-1].replace('-', '')
                else:
                    self.factura['total'] = ' '.join(row.split())\
                        .split()[-1]

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
    dir = 'Tests/MAKRO'
    if len(files) == 0:
        #dir += '/test'
        files = os.listdir(dir)
    for file in files:
        if '.pdf' in file:
            pdf = f"{dir}/{file}"
            print(f'Item: {file}')
            try:
                M = Makro(pdf)
                name, factura = M.result()
                if verbose:
                    my_print(factura)
                if txt:
                    txt = dir + '/txt/' + file.replace('.pdf', '.txt')
                    to_txt(txt, factura)
            except PermissionError:
                pass


if __name__ == '__main__':
    file = ['21-12-14 - MAKRO - 0-0(014)0009-(2021)348124.pdf']
    #file = list()
    run(file, txt=False, verbose=True)

# __NOTES__ #
'''
Nota 1:
    la esatructura ' '.join(string.split()) ha sido hallada en stackoverflow
    (como no) y su funcion viene a ser la de eliminar los espacios en blanco
    innecesarios en la cadena que se ponga como 'string'
'''
# __BIBLIOGRAPHY__ #
'''
    W3Schools:      https://www.w3schools.com/python/python_reference.asp
    stackoverflow:  https://stackoverflow.com/
'''
