#!/usr/bin/env python2

import sys
from optparse import OptionParser
import parse.py

def loadExpr():
    """Lê uma expressão (entrada via teclado)."""
    expr = raw_input(u'Expressão: ')
    return parse(expr)

def interactiveMode():
    """Inicia o modo interativo."""
    ast = loadExpr()
    bsteps = appy(ast)
    print u'Para avançar para o próximo passo digite n, para voltar p'

    index = 0
    while True:    
        print index, "->", synthetize(bstep[index])
        op = raw_input('~ ')
        if op.lower() == 'p':
            index = index - 1
        elif op.tolower() == 'n':
            index = index + 1
        if index >= len(bstep):
            break
        elif index < 0:
            index = 0
        
    print u'Expressão final:', synthetize(bsteps[-1])
    print u'Número de passos:', len(bsteps)
     
def main():
    interactive = sys.stdin.isatty() and sys.stdout.isatty()

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-m', '--machine', dest="machine_file",
                      help="File to read expression from, instead of stdin.")
    parser.add_option('-b', '--batch',
                      action="store_false", dest="interactive",
                      help="Run in batch mode: Evaluates the expression an retuns
                        normal form.")
    parser.add_option('-i', '--interactive',
                      action="store_true",  dest="interactive", default=interactive,
                      help="Run in interactive mode: Reads an input and evaluate
                        expression step-by-step.")

    options, args = parser.parse_args()
    
    if(interactive):
        interactiveMode(); 
    else:
        batchMode();

if __name__ == '__main__':
    main()
