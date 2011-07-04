# data Expr = '(' PExpr ')' | PExpr
# data PExpr = Var | LExpr | Apply
# data Var = 'a'..'z'
# data LExpr = '$' Var ( '.' Expr )?
# data Apply = Expr Expr

import re

token_re = re.compile(r'\s*(?:(\w+)|(\$)|(\.)|(\()|(\))|(.))')
VAR = 1; LAMBDA = 2; DOT = 3; L_PAREN = 4; R_PAREN = 5; ERROR = 6

# $x.$y.x y x
# (S_LAMBDA, 'x', (S_LAMBDA, 'y', (S_APPLY, (S_APPLY, (S_VAR, 'x'), (S_VAR, 'y') ), (S_VAR, 'x'))))

# (S_LAMBDA, var_name, contents)
# (S_APPLY, lhs, rhs)
# (S_VAR, var_name)
S_LAMBDA = 0; S_APPLY = 1; S_VAR = 2

class TokenizationError(Exception):
    def __init__(self, msg):
        super(TokenizationError, self).__init__(msg)

def tokenize(string):
    for m in token_re.finditer(string):
        if m.lastindex == ERROR:
            raise TokenizationError("Unknown token `%s`" % (m.group(m.lastindex)))
        else:
            yield (m.lastindex, m.group(m.lastindex))

class ParseError(Exception):
    def __init__(self, msg):
        super(ParseError, self).__init__(msg)

def tryParseVar(tokens):
    if tokens[0][0] == VAR:
        t, v = tokens.pop(0)
        return (S_VAR, v)
    else:
        return None

def tryParseLExpr(tokens):
    if tokens[0][0] == LAMBDA:
        tokens.pop(0)
        if tokens[0][0] != VAR:
            raise ParseError("Expected Var")
        t, var = tokens.pop(0)
        body = None
        if tokens[0][0] == DOT:
            tokens.pop(0)
            body = tryParseExpr(tokens)
            if body is None:
                raise ParseError("Expected PExpr")
        return (S_LAMBDA, var, body)
    else:
        return None

def tryParseApply(tokens):
    lhs = tryParseExpr(tokens)
    rhs = tryParseExpr(tokens)
    return (S_APPLY, lhs, rhs)

def tryParsePExpr(tokens):
    m = tryParseVar(tokens)
    if m is None:
        m = tryParseLExpr(tokens)
        if m is None:
            return tryParseApply(tokens)
    return m

def tryParseExpr(tokens):
    if tokens[0][0] == L_PAREN:
        t, v = tokens.pop(0)
        val = tryParsePExpr(tokens)
        if tokens[0][0] != R_PAREN:
            raise ParseError("Expected `)`")
        t, v = tokens.pop(0)
        return val
    else:
        return tryParsePExpr(tokens)
        raise ParseError("Expected Var, LExpr or Apply")

# String -> AST
def parse(string):
    return tryParseExpr(list(tokenize(string)))

# AST -> String
def synthetize(ast):
    if ast[0] == S_VAR:
        return ast[1]
    elif ast[0] == S_LAMBDA:
        return '$%s.(%s)' % (ast[1], synthetize(ast[2]))
    elif ast[0] == S_APPLY:
        return '(%s %s)' % (synthetize(ast[1]), synthetize(ast[2]))

__all__ = ['parse', 'synthetize', 'S_LAMBDA', 'S_APPLY', 'S_VAR', 'TokenizationError', 'ParseError']
