# Apply = Expr+
# Expr = LExpr | ApplyParen | Var
# LExpr = '$' Var ( '.' Apply )?
# ApplyParen = '(' Apply ')'
# Var = 'a'..'z'

import re

token_re = re.compile(r'\s*(?:(\w+)|(\$)|(\.)|(\()|(\))|(.))')
VAR = 1; LAMBDA = 2; DOT = 3; L_PAREN = 4; R_PAREN = 5; ERROR = 6; EOF = 7

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

def parseVar(tokens):
    t, v = tokens.pop(0)
    if t != VAR:
        raise ParseError("Expected Var")
    return (S_VAR, v)

def parseApplyParen(tokens):
    t, v = tokens.pop(0)
    if t != L_PAREN:
        raise ParseError("Expected `(`")
    expr = parseApply(tokens)
    t, v = tokens.pop(0)
    if t != R_PAREN:
        raise ParseError("Expected `)`")
    return expr

def parseLExpr(tokens):
    t, v = tokens.pop(0)
    if t != LAMBDA:
        raise ParseError("Expected `$`")
    t, var = tokens.pop(0)
    if t != VAR:
        raise ParseError("Expected Var")
    if tokens[0][0] == DOT:
        t, v = tokens.pop(0)
        if t != DOT:
            raise ParseError("Expected `.`")
        body = parseApply(tokens)
    else:
        body = None
    return (S_LAMBDA, var, body)

def parseExpr(tokens):
    peek = tokens[0][0]
    if peek == LAMBDA:
        return parseLExpr(tokens)
    elif peek == L_PAREN:
        return parseApplyParen(tokens)
    elif peek == VAR:
        return parseVar(tokens)
    else:
        raise ParseError("Expected LExpr, Apply or Var")

def makeApplyTree(expr_list):
    if len(expr_list) == 1:
        return expr_list[0]
    else:
        return (S_APPLY, makeApplyTree(expr_list[:-1]), expr_list[-1])

def parseApply(tokens):
    expr_list = []

    peek = tokens[0][0]
    while peek != R_PAREN and peek != EOF:
        expr_list.append(parseExpr(tokens))
        peek = tokens[0][0]

    return makeApplyTree(expr_list)

# String -> AST
def parse(string):
    token_list = list(tokenize(string))
    token_list.append((EOF, ''))
    ast = parseApply(token_list)
    if token_list[0][0] != EOF:
        raise ParseError("Unexpected trailing input: %s" % (token_list[0][1],))
    return ast

# AST -> String
def synthetize(ast):
    if ast[0] == S_VAR:
        return ast[1]
    elif ast[0] == S_LAMBDA:
        return '$%s.(%s)' % (ast[1], synthetize(ast[2]))
    elif ast[0] == S_APPLY:
        return '(%s %s)' % (synthetize(ast[1]), synthetize(ast[2]))

__all__ = ['parse', 'synthetize', 'S_LAMBDA', 'S_APPLY', 'S_VAR', 'TokenizationError', 'ParseError']
