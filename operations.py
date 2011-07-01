#retorna uma lista com as variaveis livres do ast.
def freeVars(ast):
    if not isRedex(ast):
        return ast
    pass


#faz a aplicacao de um redex (reduz ele).
#retorna uma tupla: (normal,num_steps).
def apply(redex):
    pass

#verifica se uma AST eh um redex.
def isRedex(ast):
    pass
