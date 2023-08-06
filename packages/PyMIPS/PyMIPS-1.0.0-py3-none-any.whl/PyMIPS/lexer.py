import sys
import re

NEWLINE = "NEWLINE"
DIRECTIVE = "DIRECTIVE"
LABEL = "LABEL"
COMMAND = "COMMAND"
REGISTER = "REGISTER"
REFERENCE = "REFERENCE"
INT = "INT"
SEPERATOR = "SEPERATOR"
PAREN = "PAREN"
STRING = "STRING"

commands = [
    # Basic Instructions
    r"syscall\s",
    r"bgezal\s",
    r"bltzal\s",
    r"addiu\s",
    r"break\s",
    r"maddu\s",
    r"msubu\s",
    r"sltiu\s",
    r"tgeiu\s",
    r"tltiu\s",
    r"addi\s",
    r"addu\s",
    r"andi\s",
    r"bgez\s",
    r"bgtz\s",
    r"beqz\s",
    r"blez\s",
    r"bltz\s",
    r"divu\s",
    r"eret\s",
    r"jalr\s",
    r"madd\s",
    r"mfhi\s",
    r"mflo\s",
    r"move\s",
    r"msub\s",
    r"mthi\s",
    r"mtlo\s",
    r"mult\s",
    r"sllv\s",
    r"slti\s",
    r"sltu\s",
    r"srav\s",
    r"srlv\s",
    r"subu\s",
    r"teqi\s",
    r"tgei\s",
    r"tgeu\s",
    r"tlti\s",
    r"tltu\s",
    r"tnei\s",
    r"xori\s",
    r"add\s",
    r"and\s",
    r"beq\s",
    r"bne\s",
    r"bnez\s",
    r"div\s",
    r"jal\s",
    r"lbu\s",
    r"lhu\s",
    r"lui\s",
    r"lwl\s",
    r"lwr\s",
    r"mul\s",
    r"nop\s",
    r"nor\s",
    r"not\s",
    r"ori\s",
    r"sll\s",
    r"slt\s",
    r"sra\s",
    r"srl\s",
    r"sub\s",
    r"swl\s",
    r"slr\s",
    r"teq\s",
    r"tge\s",
    r"tlt\s",
    r"tne\s",
    r"xor\s",
    r"la\s",
    r"jr\s",
    r"lb\s",
    r"lh\s",
    r"ll\s",
    r"lw\s",
    r"or\s",
    r"sb\s",
    r"sc\s",
    r"sh\s",
    r"sw\s",
    r"j\s",
    r"li\s",
    r"bge\s",
]
registers = [r"[$][^\s,)]+"]


token_exprs = (
    [
        (r"[\n\r]+", None),
        (r"[\s]+", None),
        (r"[#]+[^\n]+", None),
        (r"[.][^\s\n]+", DIRECTIVE),
        (r"[^\s]+[:]", LABEL),
        (r'".+"', STRING),
    ]
    + [(c, COMMAND) for c in commands]
    + [(r"[,]", SEPERATOR)]
    + [(r"[()]", PAREN)]
    + [(r, REGISTER) for r in registers]
    + [(r"0x[0-9]+", INT), (r"[+-]?\d+", INT), (r"[A-Za-z][A-Za-z0-9_]*", REFERENCE)]
)


def lex(characters):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    if tag == COMMAND:
                        text = text[:-1]
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write(f"Illegal character at pos {pos}: {characters[pos]}\n")
            print(characters[pos - 5 : pos + 5])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
