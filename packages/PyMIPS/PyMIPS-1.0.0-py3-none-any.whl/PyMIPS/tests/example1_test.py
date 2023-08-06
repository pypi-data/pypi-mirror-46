from PyMIPS.Datastructure.instruction_types import IType, RType, JType
from PyMIPS.Datastructure.execution_stack import run_from_list
from PyMIPS.Datastructure.data_model import DataHeap, DataStack
from PyMIPS.Datastructure.memory import Memory


def test_example1():
    try:
        DataStack.alloc(1024)
        DataHeap.alloc(1024)
        DataHeap.store_word(12, "value")
        DataHeap.store_word(0, "Z")
        exe = [0, 1, 2, 3, 4, 5]
        exe[0] = IType("li", "$t2", 25)
        exe[1] = IType("lw", "$t3", "value")
        exe[2] = RType("add", "$t4", "$t2", "$t3")
        exe[3] = RType("sub", "$t5", "$t2", "$t3")
        exe[4] = IType("sw", "$t5", "Z")
        exe[5] = IType("sw", "$t4", 4, "$sp")  # sw $t4, 4($sp)
        res = run_from_list(exe) == True
    except:
        res = False
    assert res
