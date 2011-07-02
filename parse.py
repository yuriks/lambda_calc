# data Expr = Var | Apply | LExpr
# data Var = 'a'..'z'
# data Apply = ( '(' Expr Expr ')' ) | ( Expr Expr )
# data LExpr = '$' Var ( '.' Expr )?

import re

token_re = re.compile(r'\s*(?:(\w+)|(\$)|(\.)|(\()|(\))|(.))')
VAR = 1; LAMBDA = 2; DOT = 3; L_PAREN = 4; R_PAREN = 5; ERROR = 6

# (S_LAMBDA, 'x', (S_LAMBDA, 'y', (S_APPLY, (S_APPLY, (S_VAR, 'x'), (S_VAR, 'y') ), (S_VAR, 'x'))))

# (S_LAMBDA, var_name, contents)
# (S_APPLY, lhs, rhs)
# (S_VAR, var_name)
S_LAMBDA = 0; S_APPLY = 1; S_VAR = 2

class TokenizationError(Exception):
	pass

def tokenize(string):
	for m in token_re.finditer(string):
		if m.lastindex == ERROR:
			raise TokenizationError
		else:
			yield (m.lastindex, m.group(m.lastindex))


# String -> AST
def parse(string):
	return None

# AST -> String
def synthetize(ast):
	return ""

__all__ = ['parse', 'synthetize', 'S_LAMBDA', 'S_APPLY', 'S_VAR', 'TokenizationError']
