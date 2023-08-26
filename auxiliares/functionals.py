'''
Author: Elidas              |   Python Version: 3.6.9
Date: 24/8/2023, 19:20:17    |   version: 0.0.1
'''

# __LIBRARIES__ #


# __MAIN CODE__ #
def clean_row(row):
    return row\
        .replace('\\xc2\\xaa', 'a')\
        .replace('\\xc3\\xba', 'u')\
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
        .replace('\\xc2\\x9c', 'U')\
        .replace('\'', ' ')\

#__AUXILIARY__#


#__Main Run__#
if __name__ == '__main__':
    pass

# __NOTES__ #
'''
'''

# __BIBLIOGRAPHY__ #
'''
'''