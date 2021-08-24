'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-24T12:16:40.836Z
Version: 0.0.0
'''

# __LYBRARIES__ #
from tika import parser


# __MAIN CODE__ #
def makro():
    # __lectura del archivo__ #
    raw = parser.from_file(
        '///Users/osgum/github/Zotz/files/21-01-07-MAKRO-02.pdf'  # Ruta completa
    )
    raw = str(raw['content'])  # Seleccionamos el contenido relevante
    # establecemos codificación
    safe_text = raw.encode('utf-8', errors='ignore')
    # separamos de froma que sea cómodo
    safe_text = str(safe_text).split('\\n')

    # nos quedamos solo con lo que interesa
    n = 0
    for item in safe_text[76:]:
        if item.find('Fin de factura') != -1:
            break
        n += 1
    safe_text = safe_text[76:76+n]

    # __Clasificación del contenido__ #
    factura = dict()
    factura['date'] = safe_text[1].split(' ')[-3]  # Fecha de la factura
    factura['num'] = safe_text[7].split('   ')[6:8]  # numero de Factura
    factura['articulos'] = list()  # lista de articulos comprados
    for item in safe_text[15:]:
        D = dict()
        if not item.startswith('-'):
            all = item.split(' ')
            print(all)
            D['code'] = all[1].split(' ')[0]  # código de articulo
            desc = str()
            for elem in all[1].split(' ')[1:]:
                desc += elem + ' '
            D['desc'] = desc[1:-1]  # descripción del articulo
            D['prec. ud'] = all[4]  # precio unitario
            try:
                D['ud pak'] = all[6].replace('  ', '')  # unidades por paquete
            except:
                D['ud pak'] = all[6].replace(' ', '')
            D['precio'] = all[9]  # precio por paquete
            D['uds'] = all[11]  # unidades compradas
            D['iva'] = all[14]  # código del iva
            factura['articulos'].append(D)  # guasrdamos la información
        elif item.startswith('-'):
            break
    # Buscamos el total de la factura
    for row in safe_text[15+len(factura['articulos']):]:
        if row.find('Total a pagar') != -1:
            factura['total'] = row.split('     ')[-1]
            break

    return factura


makro()


'''print('--- safe text ---')
for item in makro():
    if item != 'articulos':
        print(f'{item} : {makro()[item]}')
    else:
        print('articulos :')
        for articulo in makro()['articulos']:
            print(f'\t{articulo}')'''


# __NOTES__ #

# __BIBLIOGRAPHY__ #
