#!/usr/bin/python3

import sys
from frontend import yacc, ParseException
from backend import parse

if __name__ == "__main__":

    text = open(sys.argv[1], "r")

    try:
        ast = yacc.parse(text.read())
    except ParseException as e:
        print(e)
    else:
        ast_file = open('ast', 'w')
        ast_file.write(str(ast))

        asm = open(sys.argv[2], 'w+')
        asm.write('# Generated from: ' + sys.argv[1] + '\n')

        parse(ast, asm)

