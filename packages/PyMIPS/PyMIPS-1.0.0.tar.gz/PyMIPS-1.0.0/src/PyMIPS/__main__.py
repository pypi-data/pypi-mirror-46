#!/usr/local/bin/python
import sys

from PyMIPS.lexer import lex
from PyMIPS.AST.ast import parse
from PyMIPS.Datastructure.execution_stack import run_program


def main(args=None):
    if len(sys.argv) == 1:
        print("Usage: pymips <path to file>")
        return
    elif len(sys.argv) > 2:
        print("Too many arguments")
        return
    else:
        filename = sys.argv[1]
        with open(filename) as file:
            characters = file.read()
        tokens = lex(characters)
        res = parse(tokens)
        run_program(res.value)


if __name__ == "__main__":
    main()
