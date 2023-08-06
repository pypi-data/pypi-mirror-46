from PyMIPS.AST.combinators import *
from PyMIPS.AST.blocks import *
from PyMIPS.lexer import *
from PyMIPS.AST.ast_utils import *


def global_directive():
    def exe(data):
        (_, ref) = data
        return Globl(ref)

    return Tag(DIRECTIVE) + Tag(REFERENCE) ^ exe


def text_parser():
    return text_statements() + Lazy(text_parser) | text_statements()


def text_statements():
    return label_block() | global_directive()


def label_block():
    def process(data):
        name, contents = data
        return Label(name, contents)

    return Tag(LABEL) + command_iterator() ^ process


def command_iterator():
    return command_list() + Lazy(command_iterator) | command_list()


def command_list():
    return i_type_with_offset() | i_type() | r_type() | syscall() | j_type()


def i_type():
    def process(data):
        return create_i_type(data)

    return (
        Tag(COMMAND)
        + ((Tag(REGISTER) + Tag(SEPERATOR) + Tag(REGISTER)) | (Tag(REGISTER)))
        + Tag(SEPERATOR)
        + (Tag(INT) | Tag(REFERENCE))
    ) ^ process


def i_type_with_offset():
    return (
        Tag(COMMAND)
        + Tag(REGISTER)
        + Tag(SEPERATOR)
        + Tag(INT)
        + Tag(PAREN)
        + Tag(REGISTER)
        + Tag(PAREN)
    ) ^ create_i_type


def r_type():
    def process(data):
        return create_r_type(data)

    return (
        Tag(COMMAND)
        + (
            (
                Tag(REGISTER)
                + Tag(SEPERATOR)
                + Tag(REGISTER)
                + Tag(SEPERATOR)
                + Tag(REGISTER)
            )
            | (Tag(REGISTER) + Tag(SEPERATOR) + Tag(REGISTER))
            | Tag(REGISTER)
        )
        ^ process
    )


def syscall():
    def process(data):
        return create_syscall()

    return Keyword("syscall", COMMAND) ^ process


def j_type():
    def process(data):
        return create_j_type(data)

    return (Keyword("j", COMMAND) | Keyword("jal", COMMAND)) + Tag(REFERENCE) ^ process
