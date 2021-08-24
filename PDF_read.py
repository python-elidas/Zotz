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
def makro(file_path):
    # __lectura del archivo__ #
    raw = parser.from_file(file_path)  # Ruta completa
    raw = str(raw['content'])  # Seleccionamos el contenido relevante
    # establecemos codificación
    safe_text = raw.encode('utf-8', errors='ignore')
    # separamos de froma que sea cómodo
    safe_text = str(safe_text).split('\\n')

    # buscamos donde empiea lo interesante
    n = 0
    for row in safe_text:
        if not row.startswith('MAKRO AUTOSERVICIO MAYORISTA'):
            n += 1
        else:
            break

    '''n = 0
    for row in safe_text:
        if not row == '':
            #row = row.replace('    ', ' ')
            print(f'{n}\t{row}')
        n += 1'''

    # nos quedamos solo con lo que interesa
    safe_text = safe_text[n:]

    # __Clasificación del contenido__ #
    sep = 0  # contador para los separadoressep
    factura = dict()
    for row in safe_text:
        # Obtenemos la fecha de la factura
        if not row.find('Fecha de venta:') == -1:
            fecha = list()
            for item in row.split(' '):
                if item != '':
                    fecha.append(item)
            factura['fecha'] = fecha[-2]

        # obtenemos el numero de la factura
        elif not row.find('Factura') == -1:
            num = list()
            for item in row.split(' '):
                if item != '':
                    num.append(item)
            factura['num'] = num[1:3]
            factura['articulos'] = list()
            factura['descuentos'] = list()

        # obtenemos los articulos comprados
        if sep == 3 and not row.startswith('-'):
            # Limpieza y organizacion de la infromación de los articulos
            if not row.startswith('*') and\
                not row == '' and\
                    not row.split(' ')[3] == '':
                all = row.split(' ')
                info = list()
                cnt = 0
                desc = str()
                for i in all:
                    if i != '' and cnt < len(all)-1:
                        if all[cnt-1] == '' and\
                                all[cnt+1] == '' and desc == '':
                            info.append(i)
                        elif all[cnt-1] == '' and\
                                all[cnt+1] == '' and desc != '':
                            info.append(desc[:-1])
                            desc = ''
                            info.append(i)
                        else:
                            if cnt != 3:
                                desc += i + ' '
                            elif cnt == 3:
                                info.append(i)
                    elif cnt == len(all)-1 and not i == '':
                        info.append(i)
                    cnt += 1
                D = {
                    'codigo': info[0], 'desc': info[1],
                    'prec ud': info[3], 'ud pac': info[4],
                    'precio': info[5], 'uds': info[6],
                    'iva': info[8],
                }
                factura['articulos'].append(D)

        if row.startswith('-') or row.find('de bultos:') != -1:
            sep += 1

        # Comprobamos si existen descuentos:
        if sep == 4 and\
            not row == '' and\
            not row.startswith('-') and\
                row.find('de bultos:') == -1:
            info = list()
            for elem in row.split(' '):
                if not elem == '':
                    info.append(elem)
            D = dict()
            D['val'] = info[-3]
            D['iva'] = info[-2]
            D['code'] = info[-1]
            factura['descuentos'].append(D)

        # Buscamos el total de la factura
        if row.find('Total a pagar') != -1:
            factura['total'] = row.split('     ')[-1]
            break

    return factura


def run():
    factura = makro(
        '///Users/osgum/Desktop/Zotz/Facturas_MAKRO/21-05-08-MAKRO-01.pdf'
    )

    print('--- safe text ---')
    for item in factura:
        if type(factura[item]) != list:
            print(f'{item} : {factura[item]}')
        else:
            print(item)
            for articulo in factura[item]:
                print(f'\t{articulo}')


if __name__ == '__main__':
    run()

# __NOTES__ #

# __BIBLIOGRAPHY__ #
