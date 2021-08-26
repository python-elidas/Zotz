'''
Author: Elidas
Email: pyro.elidas@gmail.com
Python version: 3.9.1
Date: 2021-08-26T11:18:58.589Z
Version: 0.0.1
'''

# __LYBRARIES__ #
import openpyxl as xls
import simpy_sqlite as SQL

# __MAIN CODE__ #


class Excel:
    def __init__(self, file):
        self.db = SQL('files/zotz_db.db')
        self._file = file
        wb = xls.load_workbook(filename=file, read_only=False)
        # self.sheets = wb.sheetnames
        self.data = wb['Datos']
        print(self.data['Q25'].value)


def run():
    file = Excel('C:/Users/osgum/Desktop/Zotz/2021-Gastos MAKRO.xlsx')


if __name__ == '__main__':
    run()

# __NOTES__ #
'''

'''

# __BIBLIOGRAPHY__ #
'''
    pypi:       https://pypi.org/project/openpyxl/
    openpyxl:   https://openpyxl.readthedocs.io/en/stable/
'''
