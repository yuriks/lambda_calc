from parse import *

#retorna uma lista com as variaveis livres do ast.
def freeVars(ast):
    if not isRedex(ast):
        return ast
    pass

#faz a aplicacao de um redex (reduz ele).
#retorna uma lista com cada arvore de cada passo.
def apply(ast):
    pass

def step(ast):
    if ast[0] == S_VAR:
        return set([ast[0]])
    elif ast[0] == S_LAMBDA:
        return set(step(ast[2])).difference(set(ast[1]))
    elif ast[0] == S_APPLY:
        pass

#verifica se uma AST eh um redex.
def isRedex(expression):
    pass

#retorna true se 'ast' nao tem variaveis livres.
def isClosed(ast):
    pass
