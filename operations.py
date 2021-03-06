from parse import *

symb_dict = {}

SUCC = (0,'n',(0,'f',(0,'x',(1,(2,'f'),(1,(1,(2,'n'),(2,'f')),(2,'x'))))))
ADD = (0,'m',(0,'n',(0,'f',(0,'x',(1,(1,(2,'m'),(2,'f')),(1,(1,(2,'n'),(2,'f')),(2,'x')))))))
ID = (0,'x',(2,'x'))

ZERO = (0,'f',(0,'x',(2,'x')))
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
    if lhs[0] == S_LAMBDA and not substIsSafe(lhs,lhs[1],rhs):
        lhs = alphaReduction(lhs[2],lhs[1],rhs)
        return (True, lhs)

    if lhs[0] == S_LAMBDA:
        return (True, replace(lhs[1], rhs, lhs[2]))
    return (False, (S_APPLY, lhs, rhs))

def betaReduction(ast):
    """
        Faz a beta reducao de AST ate o seu estado normal.
        Retorna uma lista com todos os passos de b-reducao
    """
    bsteps = []
    go = True
    while(go):
        bsteps.append(ast)
        go, ast = step(ast)
    bsteps.append(ast)
    return bsteps 

def substIsSafe(exp1, var, exp2):
    """
        Verifica se a substituicao de var por exp2 em exp1 eh segura.
    """
    fvars2 = freeVars(exp2)
    nexp = alphaReduction(exp1,var,exp2)

    fvarsn = freeVars(nexp)

    isValid = (set(fvarsn).intersection(set(fvars2)) == set(fvars2))

    return isValid

def alphaReduction(exp1,var,exp2):
    """
        faz a reducao alpha da variavel var de exp1 relativo a exp2.
    """
    if exp1[0] == S_VAR:
        if exp1[1] == var:
            return exp2
        else:
            return exp1
    elif exp1[0] == S_LAMBDA:
        if exp1[1] == var:
            return exp1
        elif exp1[1] not in freeVars(exp2):
            return (S_LAMBDA, exp1[1], alphaReduction(exp1[2],var,exp2))
        else:
            lamt = exp1[1] + '\''
            fvars = freeVars(exp1[2]).union(freeVars(exp2))
            while(lamt == var or lamt in fvars):
                lamt = lamt + '\''

            nexp1 = alphaReduction(exp1[2],exp1[1],(S_VAR,lamt))
            return (S_LAMBDA, lamt, alphaReduction(nexp1,var,exp2))

    elif exp1[0] == S_APPLY:
        lhs = exp1[1]
        rhs = exp1[2]
        return (S_APPLY, alphaReduction(lhs,var,exp2), alphaReduction(rhs,var,exp2))


def step(ast):
    """
        Faz uma etapa da beta reducao de AST.
    """
    if ast[0] == S_VAR:
        if ast[1] in symb_dict:
            return (True, symb_dict[ast[1]])
        else:
            return (False, ast)
    elif ast[0] == S_LAMBDA:
        did_step, body = step(ast[2])
        return (did_step, (ast[0],ast[1],body))
    elif ast[0] == S_APPLY:
        did_step1, lhs = step(ast[1])
        did_step2, rhs = step(ast[2])

        did_step = did_step1 or did_step2

        ast = (ast[0],lhs,rhs)

        if not did_step:
            did_step, result = betaApply(ast[1],ast[2])
        else:
            result = ast

        return (did_step, result)

def hasRedex(exp):
    """ 
        Verifica se uma expressao eh um redex.
        Duvida: Quando uma expressao eh um redex? R. pg 151, cap. 5.
    """

    if exp[0] == S_VAR:
        return False
    if exp[0] == S_LAMBDA:
        return hasRedex(exp[2])
    if exp[0] == S_APPLY:
        lhs = exp[1]
        rhs = exp[2]

        if lhs[0] == S_LAMBDA:
            return True
        else:
            return hasRedex(lhs) or hasRedex(rhs)
