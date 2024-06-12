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
class PDF:
    def __init__(self, file='C:/Users/Elidas/github/Zotz/files/Extras/2022/LIDL/22-01-03 - LIDL - 2022044900182.pdf'):
        __reader = PdfReader(file)
        self.__pages = __reader.pages
        self.__get_text_as_list()

    def __get_text_as_list(self):
        self.__info = [page.extract_text().split('\n')
                       for page in self.__pages]
        
    def get_bill_numer(self):
        pass

    def print_pages(self):
        print([page.extract_text() for page in self.__pages])

    def print_info(self):
        [print(row) for page in self.__info for row in page]



# __Main Run__#
if __name__ == '__main__':
    item = PDF()
    item.print_pages()
    # item.print_info()

# __NOTES__ #
'''
'''

# __BIBLIOGRAPHY__ #
'''
'''
