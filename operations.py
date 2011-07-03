from parse import *

SUCC = (0,'n',(0,'f',(0,'x',(1,(2,'f'),(1,(2,'n'),(1,(2,'f'),(2,'x')))))))
ID = (0,'x',(2,'x'))

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
    elif term[0] == S_APPLY:
        lhs = replace(lam_term,new_exp,term[1])
        rhs = replace(lam_term,new_exp,term[2])
        return (term[0],lhs,rhs)

#faz a aplicacao de um redex (reduz ele).
def reduct(redex):
    exp1 = redex[1]
    if not exp1[0] == S_LAMBDA:
        return redex

    exp2 = redex[2]

    return replace(exp1[1], exp2, exp1[2])

def betaReduction(ast):
    pass
         

def step(ast):
    print 'Etapa: ' + str(ast)
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
    empty = set()
    return freeVars(exp) == empty
    

#retorna true se 'ast' nao tem variaveis livres.
def isClosed(ast):
    pass
