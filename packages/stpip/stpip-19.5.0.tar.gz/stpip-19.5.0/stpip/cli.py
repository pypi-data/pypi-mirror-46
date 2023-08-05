'''
---stpip---
This file organises the command line interface

@R. Thomas
@Santiago, Chile
@2019
'''


##standard library
import argparse

#local import
from . import __info__ as info


def command_line(args):
    '''
    This function defines the command line interface of the program.

    Parameters
    -----------
    None

    Returns
    -------
    args    Namespace with arguments
    '''

    ##create parser object
    parser = argparse.ArgumentParser(description='A pepy.tech web scraping for pypi download stats, version %s, \
            Licence: GPL'%(info.__version__))


    ###optional arguments
    parser.add_argument('-p', help='file, or list of file separated by comas (no space)')
    parser.add_argument('-w', help='if you just want the last week download counts' , action='store_true')
    parser.add_argument('-m', help='if you just want the last month download counts' , action='store_true')
    parser.add_argument('-t', help='if you just want download counts all time' , action='store_true')
    parser.add_argument('--version', help='Display the version of stpip', action='store_true')

    ##create a group of arguments that are mandatory
    return parser.parse_args(args)
