from PyMIPS.AST.combinators import *
from PyMIPS.AST.blocks import *
from PyMIPS.lexer import *
from PyMIPS.AST.ast_utils import *
from PyMIPS.Datastructure.data_commands import *


def data_parser():
    return data_statements() + Lazy(data_parser) | data_statements()


def data_statements():
    return word_directive() | asciiz_directive() | space_directive()


def word_directive():
    def exe(data):
        return DataWord(data)

    return Tag(LABEL) + Keyword(".word", DIRECTIVE) + Tag(INT) ^ exe


def asciiz_directive():
    def exe(data):
        return DataAsciiz(data)

    return Tag(LABEL) + Keyword(".asciiz", DIRECTIVE) + Tag(STRING) ^ exe


def space_directive():
    def exe(data):
        return DataSpace(data)

    return Tag(LABEL) + Keyword(".space", DIRECTIVE) + Tag(INT) ^ exe

# TODO: Add other data directives

