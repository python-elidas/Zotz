'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-24
Version: 1.0.0
'''

# __LYBRARIES__ #
import os as file
from PDF_read import makro

# __MAIN CODE__ #
dir = 'C:/Users/osgum/Desktop/Zotz/Facturas_MAKRO'
files = file.listdir(dir)
for item in files:
    try:
        print(f'Item: {item}')
        txt = dir + '/txt/' + item.replace('.pdf', '.txt')
        pdf = dir.replace('C:', '//') + '/' + item
        factura = makro(pdf)
        info = open(txt, 'w')
        for item in factura:
            if type(factura[item]) != list:
                info.write(f'{item} : {factura[item]}\n')
            else:
                info.write(f'{item}\n')
                for articulo in factura[item]:
                    info.write(f'\t{articulo}\n')
        info.close()
    except PermissionError:
        pass
# __NOTES__ #

# __BIBLIOGRAPHY__ #
