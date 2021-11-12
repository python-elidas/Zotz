'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-24
Version: 1.0.0
'''

# __LYBRARIES__ #
from tika import parser


# __MAIN CODE__ #
class Makro:
    def __init__(self, file_path):
        self.file = file_path.split('/')[-1]\
            .split('.')[0].replace('-MAKRO', '')
        # __lectura del archivo__ #
        raw = parser.from_file(file_path)  # Ruta completa
        raw = str(raw['content'])  # Seleccionamos el contenido relevante
        # establecemos codificación
        safe_text = raw.encode('utf-8', errors='ignore')
        # separamos de froma que sea cómodo
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
        # Obtenemos los articulos:
        self.get_items()
        # verificamos la existencia de descuentos
        self.get_disc()
        # Obtenemos el total de la factura:
        self.get_ammont()

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
                self.factura[row[0][:-15]] = row[1].split(' ')[1]
                self.safe_text = self.safe_text[n:]
                break
            if not bool and not row.find('Factura') == -1:
                row = row.split('  ')
                while row.count('') != 0:
                    row.remove('')
                self.factura[row[0]] = row[1:3]
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

    def get_items(self):
        n = 0
        # creamos la lista que almacenará los articulos
        self.factura['articulos'] = list()
        # creamos la lista con los códigos de los descuentos
        self.desc = list()
        for row in self.safe_text:
            D = dict()  # Los articulos se almacenan en forma de diccionario
            n += 1
            if not row.startswith('-'):
                # eliminamos los carácteres extraños
                row = row.replace('\\xc3\\x91', 'N')
                # solo se tienen en cuenta las filas con infromacion relevante
                if len(row) > 100:
                    D['codigo'] = ' '.join(row[3:18].split())  # Nota 1
                    D['desc'] = ' '.join(row[18:52].split())
                    D['prec ud'] = float(' '.join(row[57:70]
                                                  .replace(',', '.').split()))
                    D['ud pac'] = float(' '.join(row[70:80]
                                                 .replace(',', '.').split()))
                    D['precio'] = float(' '.join(row[80:90]
                                                 .replace(',', '.').split()))
                    D['uds'] = int(' '.join(row[90:99].split()))
                    D['iva'] = int(' '.join(row[108:112].split()))
                    self.factura['articulos'].append(D)
                    if not row[118:126] == '':
                        self.desc.append(row[118:126])
            else:
                self.safe_text = self.safe_text[n:]
                break

    def get_disc(self):
        n = 0
        self.factura['descuentos'] = list()
        for row in self.safe_text:
            if self.desc and not row.startswith('-'):
                row = ' '.join(row.split()).split()
                D = dict()
                D['val'] = float(row[-3][:-1].replace(',', '.')) * -1
                D['iva'] = int(row[-2])
                D['code'] = row[-1]
                self.factura['descuentos'].append(D)
            elif row.startswith('-') and n < 1:
                self.safe_text = self.safe_text[n:]
                break

    def get_ammont(self):
        for row in self.safe_text:
            if not row.find('Total a pagar') == -1:
                self.factura['total'] = ' '.join(row.split()).split()[-1]

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


def run():
    import os as file
    dir = 'C:/Users/osgum/Desktop/Zotz/Facturas_MAKRO'
    files = ['21-05-08-MAKRO-01.pdf']
    # files = file.listdir(dir)
    for item in files:
        print(f'Item: {item}')
        try:
            pdf = dir.replace('C:', '//') + '/' + item
            # txt = dir + '/txt/' + item.replace('.pdf', '.txt')
            M = Makro(pdf)
            name, factura = M.result()
            # my_print(factura)
            # to_txt(txt, factura)
        except PermissionError:
            pass


if __name__ == '__main__':
    run()

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
