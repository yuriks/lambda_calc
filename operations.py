from parse import *

#retorna uma lista com as variaveis livres do ast.
def freeVars(ast):
    if ast[0] == S_VAR:
        return set([ast[1]])
    elif ast[0] == S_LAMBDA:
        return set(freeVars(ast[2])).difference(set([ast[1]]))
    elif ast[0] == S_APPLY:
        return set(freeVars(ast[1])).union(set(freeVars(ast[2])))

#lam_term eh o nome do termo lambda. Ex.: $x.t (x eh o termo lambda).
#faz a substituicao de lam_term por new_exp em term.
def replace(lam_term, new_exp, term):
    if term[0] == S_VAR:
        if term[1] == lam_term:
            return new_exp
        else:
            return term
    elif term[0] == S_LAMBDA:
        new_term = replace(lam_term,new_exp,term[2])
        return (term[0], term[1], new_term)

#faz a aplicacao de um redex (reduz ele).
def reduct(redex):
    exp1 = redex[1]
    if not exp1[0] == S_LAMBDA:
        return redex

    exp2 = redex[2]

    new_term = replace(exp1[1], exp2, exp1[2])
    res = (exp1[0],exp1[1],new_term)
    return res

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
