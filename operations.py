from parse import *

#retorna uma lista com as variaveis livres do ast.
def freeVars(ast):
    if ast[0] == S_VAR:
        return set([ast[1]])
    elif ast[0] == S_LAMBDA:
        return set(freeVars(ast[2])).difference(set([ast[1]]))
    elif ast[0] == S_APPLY:
        return set(freeVars(ast[1])).union(set(freeVars(ast[2])))

#faz a substituicao de lam_term por new_exp em term.
def replace(lam_term, new_exp, term):
    #todo fazer recursivamente.
    pass

#faz a aplicacao de um redex (reduz ele).
def reduct(redex):
    exp1 = redex[1]
    if not exp1[0] == S_LAMBDA:
        return redex

    exp2 = redex[2]

    lam_term = exp1[1]
    return exp1[2].replace(lam_term, exp2)

def betaReduction(ast):
    pass
         

def step(ast):
    if ast[0] == S_APPLY and isRedex(ast):
        ast = reduct(ast)
    elif ast[0] == S_LAMBDA:
        s = step(ast[2])
        res = (ast[0],ast[1],s)
        ast = s
    elif ast[0] == S_VAR:
        pass
    return ast


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
