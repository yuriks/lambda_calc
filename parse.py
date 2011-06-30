# data Expr = Var | Apply | LExpr
# data Var = 'a'..'z'
# data Apply = ( '(' Expr Expr ')' ) | ( Expr Expr )
# data LExpr = '$' Var ( '.' Expr )?

# String -> AST
def parse(string):
	pass

# AST -> String
def synthetize(ast):
	return ""
