'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-24
Version: 1.0.0
'''

# __LYBRARIES__ #
from tika import parser
import hashlib as hash
from auxiliares.toolPrint import dictPrint

# __MAIN CODE__ #
class Lidl:
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
        #print(raw.keys())
        #![print(i) for i in raw['content'].split('\n\n')]
        # self.print_info(raw)
        self.clean(raw)
        # creamos el diccionario que devolveremos al final
        self.factura = dict()
        # obtenemos la fecha de la factura:
        self.get_date()
        # Obtenemos el numero de factura:
        self.get_bill_num()
        pages = list(raw['metadata'].keys())[-1]
        for i in range(int(raw['metadata'][pages])):
            #!print(f'Página {i}')
            # Quitamos mas morralla
            self.clean2()
            #! [print(row) for row in self.safe_text if i > 0]
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
                except Exception as e:
                    #print(e)
                    self.get_disc_v2()
        # Obtenemos el total de la factura:
        self.get_ammont()
        # self.my_print()
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
        for item in raw['content'].split('\n\n'):
            if not item.startswith('LIDL'):
                n += 1
            else:
                break
        self.safe_text = raw['content'].split('\n\n')[n:]
        #![print(f'clean: {row}') for row in self.safe_text]

    def get_date(self):
        month = {
            'Ene' : '01', 'Feb' : '02', 
            'Mar' : '03', 'Abr' : '04',
            'May' : '05', 'Jun' : '06',
            'Jul' : '07', 'Ago' : '08',
            'Sep' : '09', 'Oct' : '10',
            'Nov' : '11', 'Dic' : '12',
        }
        for row in self.safe_text:
            if row.startswith('Fecha Tique'):
                d = row.split(':')[-1].strip().split('-')
                d = f'{d[0]}/{month[d[1]]}/{d[2]}'
                self.factura['fecha'] = d
                
    def get_bill_num(self):
        self.factura['Factura'] = list()
        self.factura['Factura'].append(self.safe_text[3])
        self.factura['Factura'].append(0)
        

    def clean2(self):  # Limpiamos las siguientes líneas
        n = 0
        for row in self.safe_text:
            if not row == 'Importe':
                n += 1
            else:
                self.safe_text = self.safe_text[n+1:]
                break
        #![print(f'clean2: {row}') for row in self.safe_text]

    def get_items(self):
        n = 0
        # creamos in diccionario con los ids de los ivas:
        iva = {'10': 1, '21': 2, '4': 5, '0': 6}
        if not 'articulos' in self.factura:
            # creamos la lista que almacenará los articulos
            self.factura['articulos'] = list()
            # Creamos la lista de descuentos por si existen descuentos inline
            self.factura['descuentos'] = list()
        # creamos la lista con los códigos de los descuentos
        self.desc = list()
        #! [print(f'[$] get_items: {row}') for row in self.safe_text]
        for row in self.safe_text:
            #!print(row)
            n += 1
            try:
                # eliminamos los carácteres extraños
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
                # solo se tienen en cuenta las filas con infromacion relevante
                row = row.split()
                if not row[-1].startswith('-'):
                    #! [print(f'[$] get_items: {row}') for row in self.safe_text]
                    D = dict()
                    self.code = self.gen_code(' '.join(row[:-6]))
                    D['codigo'] = self.code
                    D['desc'] = ' '.join(row[:-6])
                    D['precio'] = float(row[-4].replace(',','.'))
                    D['ud pac'] = float(1)
                    D['prec ud'] = float(
                        f"{row[-1].split(',')[-2][2:]}.{row[-1].split(',')[-1]}")
                    D['uds'] = float(row[-6].replace(',','.'))
                    D['iva'] =  iva[row[-3].split(',')[0]]
                    #print(n)
                    self.factura['articulos'].append(D)
                elif row[-1].startswith('-'):
                    d = dict()
                    d['val'] = float(f"{row[-1].split(',')[-2][2:]}.{row[-1].split(',')[-1]}")
                    d['iva'] = iva[row[-3].split(',')[0]]
                    d['code'] = self.code
                    self.factura['descuentos'].append(d)
            except Exception as e:
                #print(e)
                self.safe_text = self.safe_text[n-1:]
                break
        #!print(self.factura['articulos'])
    
    def gen_code(self, string):
        '''if string.startswith('Desc'):
            string = 'descuento'''
        model = hash.new('sha256')
        model.update(string.encode('utf-8'))
        return model.hexdigest()[:10]

    def get_items_v2(self):
            pass
        
    def get_disc(self):
        pass
    
    def get_disc_v2(self):
        pass

    def get_ammont(self):
        self.factura['total'] = self.safe_text[0]

    def result(self):
        return self.file, self.factura

    def my_print(self):
        for key in self.factura.keys():
            print(f'{key}\n')
            if type(self.factura[key]) is list:
                for item in self.factura[key]:
                    print(f'\t{item}')
            else:
                print(f'\t{self.factura[key]}')

    def to_txt(self, txt):
        info = open(txt, 'w')
        for item in self.factura:
            if type(self.factura[item]) != list:
                info.write(f'{item} : {self.factura[item]}\n')
            else:
                info.write(f'{item}\n')
                for articulo in self.factura[item]:
                    info.write(f'\t{articulo}\n')
        info.close()


def run(files, txt=False, verbose=True):
    import os
    dir = 'Tests/LIDL'
    if len(files) == 0:
        files = os.listdir(dir)
    for file in files:
        pdf = f"{dir}/{file}"
        print(f'Item: {file}')
        try:
            M = Lidl(pdf)
            name, factura = M.result()
            if verbose:
                M.my_print()
            if txt:
                txt = dir + '/txt/' + file.replace('.pdf', '.txt')
                M.to_txt(txt)
        except PermissionError:
            pass


if __name__ == '__main__':
    #file = ['21-03-04 - LIDL - 2022401600218.pdf']
    file = list()
    run(file, txt=False, verbose=True)

# __NOTES__ #
'''
Ciertas cosas se quedan por herencia del fichero.

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
