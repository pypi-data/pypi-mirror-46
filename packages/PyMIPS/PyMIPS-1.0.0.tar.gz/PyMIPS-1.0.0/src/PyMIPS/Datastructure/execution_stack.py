from PyMIPS.Datastructure.data_model import (
    ProgramStack,
    RegisterPool,
    DataStack,
    DataHeap,
)
from PyMIPS.Datastructure.memory import Memory
from PyMIPS.AST.blocks import Program


def run_from_list(commands: list):

    iteration = 0
    for c in commands:
        print(f"({iteration}): {str(c)}")
        c()
        print()
        iteration += 1
    return True


def run_program(p: Program):
    # Reset everything
    Memory.reset()
    ProgramStack.reset
    DataHeap.reset()

    # Allocate data block
    p.data()

    # Push the instructions to program stack
    ProgramStack.add_text_block(p.text)

    # Set the program counter
    p.globl()

    # Run the program
    print(p)
    print("----------------------\nSTART OF PROGRAM")
    while True:
        try:
            ProgramStack.execute_next()
            # RegisterPool.print_all_active_registers()
        except Exception as e:
            print(e)
            break
