'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9
Date: 2021-01-24
Version: 1.0.0
'''

# __LIBRARIES__ #
import os as file
import shutil
from tkinter import messagebox

# __MAIN CODE__ #
def get_xcl_name(f_dir):
    for dir in file.listdir(f_dir):
        if 'pdf' in dir.split('.')[-1]:
            Y = '20' + dir.split(' - ')[0].split('-')[0]
            prov = dir.split(' - ')[1]
            break
    return f'Facturas {prov} {Y}'
    
def find_excel(xcl_dir, f_dir):
    name = get_xcl_name(f_dir)
    for dir in file.listdir(xcl_dir):
        if 'xlsx' in dir.split('.')[-1]: # Miramos la extension de los archivos
            # si existe un excel miramos que sea el que debemos emplear
            if name in dir.split('.')[0]:
                return True
    return False

def create_new_excl(xcl_dir, f_dir):
    nme = get_xcl_name(f_dir)
    messagebox.showinfo(
        title='Excel no encontrado.',
        message=f'Se creará un excel con el nombre {nme}\nen la carpeta seleccionada.'
    )
    src = f'{file.getcwd()}\\files\\{nme.split(" ")[1]}.xlsx'
    dst = f'{xcl_dir}\\{nme}.xlsx'
    shutil.copy2(src, dst)
    return nme
    
    
if __name__ == '__main__':
    pass
    
# __NOTES__ #
'''

'''

# __BIBLIOGRAPHY__ #
'''
    

'''
