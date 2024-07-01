'''
Author: Elidas              |   Python Version: 3.9.9
Date: 11/6/2024, 12:39:50   |   version: 0.0.1
'''

# __LIBRARIES__ #
import openpyxl as xlsx
from pypdf import PdfReader
from tkinter import messagebox, filedialog
if __name__ == '__main__':
    from functionals import clean_row
    from toolPrint import dictPrint
else:
    from auxiliares.functionals import clean_row
    from auxiliares.toolPrint import dictPrint

# __AUXILIARY__#


# __MAIN CODE__ #
class Makro:
    def __init__(self, file_path='C:/Users/Elidas/github/Zotz/files/Extras/2022/MAKRO/22-01-10 - MAKRO - 0-0(014)0010-(2022)010015.pdf'):
        __reader = PdfReader(file_path)
        # Obtenemos el nombre de la factura para plasmarlo en el Excel
        self.__file_name = file_path.split('/')[-1].split('.')[0].split(' - ')[-1]
        self.__pages = __reader.pages
        self.__get_text_as_list()
        self.__clean_info()
        self.__get_bill_number()

    def __get_text_as_list(self):
        self.__info = [page.extract_text().split('\n') for page in self.__pages]
        
    def __clean_info(self):
        clean = list()
        for page in self.__info:
            for row in page:
                clean_row = list()
                for item in row.split(' '):
                    if len(item) > 1:
                        clean_row.append(item)
                clean.append('\t'.join(clean_row))
        self.__info = clean

    def __get_bill_date(self):
        pass
    
    def __get_bill_number(self):
        for row in self.__info:
            if 'Factura' in row:
                pass

    def print_info(self):
        with open('makro_info.txt', 'w') as fw:
            for row in self.__info:
                    fw.write(row + '\n')
                            


# __Main Run__#
if __name__ == '__main__':
    item = Makro()
    #item.print_pages()
    #item.print_info()

# __NOTES__ #
'''
'''

# __BIBLIOGRAPHY__ #
'''
'''
