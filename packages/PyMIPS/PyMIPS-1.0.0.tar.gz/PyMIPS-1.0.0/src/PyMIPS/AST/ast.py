from PyMIPS.AST.combinators import *
from PyMIPS.AST.blocks import *
from PyMIPS.lexer import *

from PyMIPS.AST.Parsers.text import text_parser, global_directive
from PyMIPS.AST.Parsers.data import data_parser


def parse(tokens):
    def process(data):
        return Program(data)

    return (asm_parser() ^ process)(tokens, 0)


def asm_parser():
    return blocks() + Lazy(asm_parser) | blocks()


def blocks():
    return global_directive() | text_block() | data_block()


def text_block():
    def process(data):
        _, contents = data
        return TextBlock(contents)

    return Keyword(".text", DIRECTIVE) + text_parser() ^ process


def data_block():
    def process(data):
        _, contents = data
        return DataBlock(contents)

    return Keyword(".data", DIRECTIVE) + data_parser() ^ process

