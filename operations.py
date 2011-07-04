from parse import *

SUCC = (0,'n',(0,'f',(0,'x',(1,(2,'f'),(1,(1,(2,'n'),(2,'f')),(2,'x'))))))
ID = (0,'k',(2,'k'))

ZERO = (0,'g',(0,'y',(2,'y')))
ONE = (1,SUCC,ZERO)
TWO = (1,SUCC,ONE)
THREE = (1,SUCC,TWO)
FOUR = (1,SUCC,THREE)
FIVE = (1,SUCC,FOUR)
SIX = (1,SUCC,FIVE)

def freeVars(ast):
    """Retorna uma lista com as variaveis livres de AST."""
    if ast[0] == S_VAR:
        return set([ast[1]])
    elif ast[0] == S_LAMBDA:
        return set(freeVars(ast[2])).difference(set([ast[1]]))
    elif ast[0] == S_APPLY:
        return set(freeVars(ast[1])).union(set(freeVars(ast[2])))

def replace(lam_term, new_exp, term):
    """
        Faz a substituicao de lam_term por new_exp em term.
        lam_term é o nome do termo lambda. Ex.: $x.t (x é o termo lambda).  
    """
    if term[0] == S_VAR:
        if term[1] == lam_term:
            return new_exp
        else:
            return term
    elif term[0] == S_LAMBDA:
        new_term = replace(lam_term,new_exp,term[2])
        return (term[0], term[1], new_term)
    elif term[0] == S_APPLY:
        lhs = replace(lam_term,new_exp,term[1])
        rhs = replace(lam_term,new_exp,term[2])
        return (term[0],lhs,rhs)

def betaApply(lhs,rhs):
    """ 
        Faz uma aplicação de rhs em lhs.
    """
    if lhs[0] == S_LAMBDA:
        return replace(lhs[1], rhs, lhs[2])
    return (S_APPLY, lhs, rhs)

def betaReduction(ast):
    """
        Faz a beta redução de AST até o seu estado normal.
    """
    result = ast
    last = None
    while(result != last):
        last = result
        result = step(result)
    return result

def step(ast):
    """
        Faz uma etapa da beta redução de AST.
    """
    if ast[0] == S_VAR:
        return ast
    elif ast[0] == S_LAMBDA:
        return (ast[0],ast[1],step(ast[2]))
    elif ast[0] == S_APPLY:# and isRedex(ast):
        lhs = step(ast[1])
        rhs = step(ast[2])
        
        if lhs == None:
            lhs = ast[1]
        if rhs == None:
            rhs = ast[2]
             
        ast = (ast[0],lhs,rhs)  
        result = betaApply(ast[1],ast[2])

        return result

def isRedex(exp):
    """ 
        Verifica se uma expressão é um redex.
        Dúvida: Quando uma expressão é um redex?
    """
    empty = set()
    return (freeVars(exp) != empty) #isso nao ta certo.

