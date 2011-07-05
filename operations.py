from parse import *

SUCC = (0,'n',(0,'f',(0,'x',(1,(2,'f'),(1,(1,(2,'n'),(2,'f')),(2,'x'))))))
ADD = (0,'m',(0,'w',(0,'q',(0,'r',(1,(1,(2,'m'),(2,'q')),(1,(1,(2,'w'),(2,'q')),(2,'r')))))))
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
        lam_term eh o nome do termo lambda. Ex.: $x.t (x eh o termo lambda).  
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
        Faz uma aplicacao de rhs em lhs.
    """
    if lhs[0] == S_LAMBDA:
        return replace(lhs[1], rhs, lhs[2])
    return (S_APPLY, lhs, rhs)

def betaReduction(ast):
    """
        Faz a beta reducao de AST ate o seu estado normal.
    """
    while(isRedex(ast)):
        ast = step(ast)
    return ast

def step(ast):
    """
        Faz uma etapa da beta reducao de AST.
    """
    if ast[0] == S_VAR:
        return ast
    elif ast[0] == S_LAMBDA:
        return (ast[0],ast[1],step(ast[2]))
    elif ast[0] == S_APPLY:
        lhs = step(ast[1])
        rhs = step(ast[2])
             
        ast = (ast[0],lhs,rhs)  
        result = betaApply(ast[1],ast[2])

        return result

def isRedex(exp):
    """ 
        Verifica se uma expressao eh um redex.
        Duvida: Quando uma expressao eh um redex? R. pg 151, cap. 5.
    """
    aux = step(exp)
    return aux != exp
