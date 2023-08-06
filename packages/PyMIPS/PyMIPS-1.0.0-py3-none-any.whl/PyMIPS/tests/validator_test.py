from PyMIPS.Datastructure.instruction_types import IType, RType, JType
from PyMIPS.AST.validator import validate
import unittest


class TestRType(unittest.TestCase):
    def test_all(self):
        try:
            RType("add", "$t3", "$t2", "$t1")
            RType("addu", "$t3", "$t2", "$t1")
            RType("and", "$t3", "$t2", "$t1")
            RType("nor", "$t3", "$t2", "$t1")
            RType("or", "$t3", "$t2", "$t1")
            RType("slt", "$t3", "$t2", "$t1")
            RType("sltu", "$t3", "$t2", "$t1")
            RType("sub", "$t3", "$t2", "$t1")
            RType("subu", "$t3", "$t2", "$t1")
            RType("xor", "$t3", "$t2", "$t1")
            RType("or", "$s0", "$t0", "$t3")
            RType("div", "$t3", "$t2")
            RType("divu", "$t3", "$t2")
            RType("jalr", "$t3", "$t2")
            RType("mult", "$t3", "$t2")
            RType("mul", "$t3", "$t2")
            RType("move", "$t3", "$t2")
            RType("jr", "$ra")
            RType("mfhi", "$t3")
            RType("mflo", "$t3")
            RType("mthi", "$t3")
            RType("mtlo", "$t3")
            RType("syscall", destination=None)
        except:
            self.fail()

    def test_bad_3(self):
        with self.assertRaises(Exception):
            RType("add", "$t3")
        with self.assertRaises(Exception):
            RType("add", "$t3df", "$tdfs", "45")
        with self.assertRaises(Exception):
            RType("sub", "$t3", "4")
        with self.assertRaises(Exception):
            RType("move", "$3", "t435", "$vew")
        with self.assertRaises(Exception):
            RType("lw", "$t3", "$s4", "gfd4")

    def test_bad_2(self):
        with self.assertRaises(Exception):
            RType("add", "$t3", "$t4")
        with self.assertRaises(Exception):
            RType("div", "$t3")
        with self.assertRaises(Exception):
            RType("mul", "$", "3")

    def test_bad_1(self):
        with self.assertRaises(Exception):
            RType("mfhi", "$t3", "$t4")
        with self.assertRaises(Exception):
            RType("mflo", None)
        with self.assertRaises(Exception):
            RType("mflo", "tr")

    def test_bad_0(self):
        with self.assertRaises(Exception):
            RType("syscall", "$t3")


class TestIType(unittest.TestCase):
    def test_all(self):
        try:
            IType("addi", "$t3", 6, "$t4")
            IType("addiu", "$t3", 6, "$t4")
            IType("andi", "$t3", 0000, "$t4")
            IType("beq", "$t3", "label", "$t4")
            IType("ori", "$t3", 6, "$t1")
            IType("xori", "$t3", 6, "$t4")
            IType("bgez", "$t3", "label")
            IType("sw", "$t0", -4, "$sp")
            IType("lw", "$t3", 5)
            IType("la", "$t3", 543)
            IType("la", "$t3", 5453, "$t2")
            IType("li", "$t0", 4)
            IType("bne", "$t0", "label", "$t8")
            IType("bltz", "$t3", "label")
            IType("lui", "$t3", 100)
            IType("tgei", "$t3", 100)

        except:
            self.fail()

    def test_bad_2(self):
        with self.assertRaises(Exception):
            IType("lw", "$t0", immediate=None)
        with self.assertRaises(Exception):
            IType("add", "$t32", 10)
        with self.assertRaises(Exception):
            IType("lw", "t32", immediate=None)
        with self.assertRaises(Exception):
            IType("addi", "$t2", "5", "$t44")
        with self.assertRaises(Exception):
            IType("la", "$t2", 5, "$t44")

    def test_bad_1(self):
        with self.assertRaises(Exception):
            IType("li", "$t3", 10, source="$t2")
        with self.assertRaises(Exception):
            IType("lui", "100", 100)
        with self.assertRaises(Exception):
            IType("la", "$t3f", 34)


class TestJType(unittest.TestCase):
    def test_all(self):
        try:
            JType("j", "func1")
            JType("jal", "func2")
            JType("jal", 1)
        except:
            self.fail()

    def test_bad(self):
        with self.assertRaises(Exception):
            JType("add", "funct1")
