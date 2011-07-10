#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from parse import *
from operations import *

def loadExpr():
    """Le uma expressao (entrada via teclado)."""
    expr = raw_input('Expressao: ')
    return parse(expr)

def interactiveMode():
    """Inicia o modo interativo."""
    ast = loadExpr()
    bsteps = betaReduction(ast)
    for sn, step in enumerate(bsteps):
        print sn, '->', synthetize(step) 
    if sys.stdin.isatty():
        op = raw_input('\nAvaliar mais expressoes (y/n)? ')
        if op.lower() == 'y':
            interactiveMode()

def batchMode(expr = None):
    if expr is None:
        expr = loadExpr()
    print synthetize(betaReduction(expr)[-1]) 
    if sys.stdin.isatty():
        if raw_input(u'Avaliar mais expressoes (y/n)? ').lower() == 'y':
            batchMode()

def main():
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-b', '--batch',
        action="store_false", dest="interactive",
        help="""Run in batch mode: Evaluates the expression an retuns
                        normal form.""")
    parser.add_option('-i', '--interactive',
        action="store_true",  dest="interactive", default=interactive,
        help="""Runs in interactive mode: Reads an lambda input and evaluate
                        expression step-by-step.""")

    options, args = parser.parse_args()

    if options.interactive == True:
        print "Modo interativo."
        interactiveMode(); 
    else:
        print "Modo batch."
        batchMode();

if __name__ == '__main__':
    main()
