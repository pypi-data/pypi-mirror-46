#!/usr/bin/./python
# -*- coding: utf-8 -*-

'''
---stpip---

stpip is a program web scrapping the pepy.tech website that displays pepy statistics.

usage: stpip --help
'''


###Python standard library
import sys

###local imports
from . import cli
from . import __info__ as info
from . import scraping
from . import display

def main():
    '''
    This is the main function of the program.
    '''
    ###first we load the command line interface
    args = cli.command_line(sys.argv[1:])

    ###here we check if at least one argument was given:
    if not args.p and not args.version:
        print('\033[1m[stpip Error]> no argument passed ...exit\033[0;0m')
        sys.exit()

    
    if args.version:
        print('version %s, Author: %s'%(info.__version__, info.__credits__))
        sys.exit()

    if args.p:
        ###extract package names from CLI
        packs = args.p.split(',')

        if len(packs)>1:
            tot = 0

        ##and go scraping!
        for i in packs:
            total, month, day, yesterday, yest_down, ndays = scraping.scrap(i)
            
            if len(packs)>1:
                tot += int(total) 

            if not args.t and not args.m and not args.w:
                display.full(total, month, day, yesterday, yest_down, ndays, i)

            elif args.t:
                display.indiv(total, 'total', i)

            elif args.m:
                display.indiv(month, 'month', i)

            elif args.w:
                display.indiv(day, 'week', i)

        if len(packs)>1:
            print('\033[1mTotal for all requested packages: %s Downloads'% tot)
