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
    raw = parser.from_file(
        '///Users/osgum/github/Zotz/files/21-01-07-MAKRO-01.pdf'  # Ruta completa
    )
    raw = str(raw['content'])  # Seleccionamos el contenido
    safe_text = raw.encode('utf-8', errors='ignore')  # establecemos codificación

    safe_text = str(safe_text).split('\\n')  # separamos de froma que sea cómodo

    return safe_text[76:]


safe_text = makro()

date = safe_text[1].split(' ')[-3]
factura = safe_text[7].split('   ')[6:8]
articulos = list()  # esto tiene que pasar a ser un diccionario
for item in safe_text[15:]:
    if not item.startswith('-'):
        articulos.append(item)
    elif item.startswith('-'):
        break
print(articulos)

print('--- safe text ---')
n = 0
for item in makro():
    print(f'{n}\t{item}')
    n += 1

# __NOTES__ #

# __BIBLIOGRAPHY__ #
