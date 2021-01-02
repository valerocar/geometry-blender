from sympy.parsing.sympy_parser import parse_expr
from sympy import exp, Symbol,  srepr

def sigmoid(k, s):
    return 1 / (1 + exp(-s / k))


# Unary functions
##################


def f_not(a):
    return 1 - a


# Binary functions
###################


def fb_and(a, b):
    return a * b


def fb_or(a, b):
    return a + b - a * b


# Multiple arguments functions
##############################


def f_and(*args):
    count = len(args)
    c = args[0]
    for i in range(1, count):
        c = fb_and(c, args[i])
    return c


def f_or(*args):
    count = len(args)
    c = args[0]
    for i in range(1, count):
        c = fb_or(c, args[i])
    return c


# Logic parser
###########################

def parse_logic(ex, d):
    sd = {}
    for k in d.keys():
        sd[Symbol(k)] = d[k]
    ex_p = parse_expr(ex)
    ex_s = srepr(ex_p)
    ex_t = ex_s.replace('Or', 'f_or').replace('And', 'f_and').replace('Not', 'f_not')
    result = eval(ex_t)
    return result.subs(d)
