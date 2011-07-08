from parse import *

SUCC = (0,'n',(0,'f',(0,'x',(1,(2,'f'),(1,(1,(2,'n'),(2,'f')),(2,'x'))))))
ADD = (0,'m',(0,'w',(0,'q',(0,'r',(1,(1,(2,'m'),(2,'q')),(1,(1,(2,'w'),(2,'q')),(2,'r')))))))
ID = (0,'k',(2,'k'))

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
        print 'not safe: %s' % synthetize(lhs)
        lhs = alphaReduction(lhs[2],lhs[2],rhs)
        print 'novo: %s' % synthetize(lhs)

    if lhs[0] == S_LAMBDA:
        return replace(lhs[1], rhs, lhs[2])
    return (S_APPLY, lhs, rhs)

def betaReduction(ast):
    """
        Faz a beta reducao de AST ate o seu estado normal.
    """
    print 'betaReduct: %s' % synthetize(ast)
    while(isRedex(ast)):
        ast = step(ast)
    return ast

def substIsSafe(exp1, var, exp2):
    """
        Verifica se a substituicao de var por exp2 em exp1 eh segura.
    """
    fvars2 = freeVars(exp2)
    nexp = replace(var,exp2,exp1)

    fvarsn = freeVars(nexp)

    isValid = (set(fvarsn).intersection(set(fvars2)) == set(fvars2))

    return isValid

def alphaReduction(exp1,var,exp2):
    """
        faz a reducao alpha da variavel var de exp1 relativo a exp2.
    """
#    a = synthetize(exp1)
#    b = synthetize(exp2)
#    print str(a) + ' [' + str(var) + '->' + str(b) + ']'
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
