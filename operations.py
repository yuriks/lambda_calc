from parse import *

#retorna uma lista com as variaveis livres do ast.
def freeVars(ast):
    if ast[0] == S_VAR:
        return set([ast[0]])
    elif ast[0] == S_LAMBDA:
        return set(step(ast[2])).difference(set(ast[1]))
    elif ast[0] == S_APPLY:
        if not isRedex(ast):
            return set([ast])

#faz a aplicacao de um redex (reduz ele).
def reduct(redex):
    exp1 = redex[1]
    exp2 = redex[2]

    exp1.replace(exp2)
    return exp1

def step(ast):
    pass

#verifica se uma expressao eh um redex.
def isRedex(exp):
    if not exp[0] == S_APPLY:
        return False
    first = exp[1]

    if not first[0] == S_LAMBDA:
        return False

    return True
    

#retorna true se 'ast' nao tem variaveis livres.
def isClosed(ast):
    pass
