#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from parse import *
from operations import *

def loadExpr():
    """Le uma expressao (entrada via teclado)."""
    expr = raw_input('Expressao: ')
    if len(expr) > 0 and expr[0] == '=':
        l = expr[1:].split(' ', 1)
        symb_dict[l[0]] = parse(l[1])
        return None
    return parse(expr)

def interactiveMode():
    """Inicia o modo interativo."""
    ast = loadExpr()
    if ast is not None:
        bsteps = betaReduction(ast)
        for sn, step in enumerate(bsteps):
            print sn, '->', synthetize(step) 
    if sys.stdin.isatty():
        interactiveMode()

def batchMode(expr = None):
    if expr is None:
        expr = loadExpr()
    if expr is not None:
        print synthetize(betaReduction(expr)[-1]) 
    if sys.stdin.isatty():
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
