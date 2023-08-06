try:
    from src.PyMIPS.Datastructure.memory import Memory
    from src.PyMIPS.Datastructure.instruction_types import (
        IType,
        JType,
        RType,
        BaseCommand,
        DataStack,
        DataHeap,
    )

    from src.PyMIPS.Datastructure.data_model import RegisterPool, ProgramStack
except:
    from PyMIPS.Datastructure.memory import Memory
    from PyMIPS.Datastructure.data_model import (
        RegisterPool,
        ProgramStack,
        DataStack,
        DataHeap,
    )
    from PyMIPS.Datastructure.instruction_types import IType, JType, RType, BaseCommand

import unittest

"""
sll, srl, and sra are treated as I Types
"""


class TestRTypes(unittest.TestCase):
    def test_sllv(self):
        r = RType("sllv", "$t0", "$t1", "$t2")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t1.set_contents_from_int(123)
        t2.set_contents_from_int(2)
        r()
        self.assertEqual(t0.get_contents_as_int(), 492)

    def test_srlv(self):
        r = RType("srlv", "$t0", "$t1", "$t2")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t1.set_contents_from_int(-16)
        t2.set_contents_from_int(2)
        r()
        self.assertEqual(t0.get_contents_as_int(), 1073741820)

    def test_srav(self):
        r = RType("srav", "$t0", "$t1", "$t2")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t1.set_contents_from_int(-16)
        t2.set_contents_from_int(2)
        r()
        self.assertEqual(t0.get_contents_as_int(), 1073741820)

    def test_jr(self):
        r = RType("jr", "$ra")
        ra = RegisterPool.get_register("$ra")
        pc = RegisterPool.get_register("pc")
        ra.set_contents_from_int(263)
        r()
        self.assertEqual(pc.get_contents_as_int(), 263)

    def test_jalr(self):
        self.skipTest("Unimplemented")
        r = RType("jalr", "$t0")
        ra = RegisterPool.get_register("$ra")
        t0 = RegisterPool.get_register("$t0")
        pc = RegisterPool.get_register("pc")
        current = pc.get_contents_as_int()
        t0.set_contents_from_int(444)
        r()
        self.assertEqual(pc.get_contents_as_int(), 444)
        self.assertEqual(ra.get_contents_as_int(), current)

    def test_jalr_2_r(self):
        self.skipTest("Unimplemented")
        r = RType("jalr", "$t1", "$t0")
        t1 = RegisterPool.get_register("$t1")
        t0 = RegisterPool.get_register("$t0")
        pc = RegisterPool.get_register("pc")
        current = pc.get_contents_as_int()
        t0.set_contents_from_int(875)
        r()
        self.assertEqual(pc.get_contents_as_int(), 875)
        self.assertEqual(t1.get_contents_as_int(), current)

    def test_syscall(self):
        # TODO: Figure this out. Ommitting for now
        pass

    def test_move(self):
        r = RType("move", "$t1", "$t2")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t2.set_contents_from_int(8134)
        r()
        self.assertEqual(t1.get_contents_as_int(), 8134)

    def test_mfhi(self):
        r = RType("mfhi", "$t1")
        t1 = RegisterPool.get_register("$t1")
        hi = RegisterPool.get_register("hi")
        hi.set_contents_from_int(280)
        r()
        self.assertEqual(t1.get_contents_as_int(), 280)

    def test_mthi(self):
        r = RType("mthi", "$t1")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(342)
        r()
        hi = RegisterPool.get_register("hi")
        self.assertEqual(hi.get_contents_as_int(), 342)

    def test_mflo(self):
        r = RType("mflo", "$t1")
        t1 = RegisterPool.get_register("$t1")
        lo = RegisterPool.get_register("lo")
        lo.set_contents_from_int(423)
        r()
        self.assertEqual(t1.get_contents_as_int(), 423)

    def test_mtlo(self):
        r = RType("mtlo", "$t1")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(564)
        r()
        lo = RegisterPool.get_register("lo")
        self.assertEqual(lo.get_contents_as_int(), 564)

    def test_mult_both_pos(self):
        r = RType("mult", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(651)
        t1.set_contents_from_int(321)
        r()
        hi = RegisterPool.get_register("hi").get_contents_as_int()
        lo = RegisterPool.get_register("lo").get_contents_as_int()
        self.assertEqual(hi, 0)
        self.assertEqual(lo, 208971)

    def test_mult_one_neg(self):
        r = RType("mult", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(651)
        t1.set_contents_from_int(-321)
        r()
        hi = RegisterPool.get_register("hi").get_contents_as_int()
        lo = RegisterPool.get_register("lo").get_contents_as_int()
        self.assertEqual(hi, -1)
        self.assertEqual(lo, -208971)

    def test_mult_both_neg(self):
        r = RType("mult", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(-651)
        t1.set_contents_from_int(-321)
        r()
        hi = RegisterPool.get_register("hi").get_contents_as_int()
        lo = RegisterPool.get_register("lo").get_contents_as_int()
        self.assertEqual(hi, 0)
        self.assertEqual(lo, 208971)

    def test_multu(self):
        self.skipTest("Unimplemented")
        r = RType("multu", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(-651)
        t1.set_contents_from_int(321)
        r()
        hi = RegisterPool.get_register("hi").get_contents_as_int()
        lo = RegisterPool.get_register("lo").get_contents_as_int()
        self.assertEqual(hi, 320)
        self.assertEqual(lo, 208971)

    def test_div(self):
        r = RType("div", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(651)
        t1.set_contents_from_int(213)
        r()
        quo = RegisterPool.get_register("lo").get_contents_as_int()
        rem = RegisterPool.get_register("hi").get_contents_as_int()
        self.assertEqual(quo, 3)
        self.assertEqual(rem, 12)

    def test_divu(self):
        self.skipTest("Unimplemented")
        r = RType("divu", "$t0", "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t0.set_contents_from_int(543)
        t1.set_contents_from_int(432)
        r()
        quo = RegisterPool.get_register("lo").get_contents_as_int()
        rem = RegisterPool.get_register("hi").get_contents_as_int()
        self.assertEqual(quo, 1)
        self.assertEqual(rem, 111)

    def test_add(self):
        r = RType("add", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(4)
        t3.set_contents_from_int(6)
        r()
        self.assertEqual(t0.get_contents_as_int(), 10)

    def test_addu(self):
        r = RType("addu", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(2147483647)
        t3.set_contents_from_int(1)
        r()
        self.assertEqual(t0.get_contents_as_unsigned_int(), 2147483648)

    def test_sub(self):
        r = RType("sub", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(1000)
        t3.set_contents_from_int(654)
        r()
        self.assertEqual(t0.get_contents_as_int(), 346)

    def test_subu(self):
        r = RType("subu", "$t0", "$t1", "$t3")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t3 = RegisterPool.get_register("$t3")
        t1.set_contents_from_int(-2147483648)
        t3.set_contents_from_int(1)
        r()
        self.assertEqual(t0.get_contents_as_int(), 2147483647)

    def test_and(self):
        r = RType("and", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(60)
        s1.set_contents_from_int(13)
        r()
        self.assertEqual(t0.get_contents_as_int(), 12)

    def test_or(self):
        r = RType("or", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(312)
        s1.set_contents_from_int(456)
        r()
        self.assertEqual(t0.get_contents_as_int(), 504)

    def test_xor(self):
        r = RType("xor", "$t0", "$s0", "$s1")
        t0 = RegisterPool.get_register("$t0")
        s0 = RegisterPool.get_register("$s0")
        s1 = RegisterPool.get_register("$s1")
        s0.set_contents_from_int(4651)
        s1.set_contents_from_int(65)
        r()
        self.assertEqual(t0.get_contents_as_int(), 4714)

    def test_nor(self):
        r = RType("nor", "$t1", "$s1", "$s2")
        t1 = RegisterPool.get_register("$t1")
        s1 = RegisterPool.get_register("$s1")
        s2 = RegisterPool.get_register("$s2")
        s1.set_contents_from_int(314)
        s2.set_contents_from_int(789)
        r()
        self.assertEqual(t1.get_contents_as_int(), -832)

    def test_slt(self):
        r = RType("slt", "$t1", "$t2", "$t3")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t3 = RegisterPool.get_register("$t3")
        t2.set_contents_from_int(2)
        t3.set_contents_from_int(3)
        r()
        self.assertEqual(t1.get_contents_as_int(), 1)

    def test_sltu(self):
        r = RType("sltu", "$t1", "$t2", "$t3")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t3 = RegisterPool.get_register("$t3")
        t2.set_contents_from_int(-2147483649)
        t3.set_contents_from_int(2147483651)
        r()
        self.assertEqual(t1.get_contents_as_int(), 1)


class TestJTypes(unittest.TestCase):
    def test_jump(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        program = {
            "main": [JType("j", "test"), BaseCommand(), BaseCommand(), BaseCommand()],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        ProgramStack.jump_label("main")
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)

    def test_jal(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        ra = RegisterPool.get_register("$ra")
        program = {
            "main": [JType("jal", "test"), BaseCommand(), BaseCommand(), BaseCommand()],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        ProgramStack.jump_label("main")
        current = pc.get_contents_as_int() + 4
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)
        self.assertEqual(ra.get_contents_as_int(), current)


class TestITypes(unittest.TestCase):
    def test_sll(self):
        i = IType("sll", "$t0", 2, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(4)
        i()
        self.assertEqual(t0.get_contents_as_int(), 16)

    def test_srl(self):
        i = IType("srl", "$t0", 4, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(123)
        i()
        self.assertEqual(t0.get_contents_as_int(), 7)

    def test_sra(self):
        i = IType("sra", "$t1", 4, "$s0")
        t1 = RegisterPool.get_register("$t1")
        s0 = RegisterPool.get_register("$s0")
        s0.set_contents_from_int(123)
        i()
        self.assertEqual(t1.get_contents_as_int(), 7)

    def test_beq_true(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        program = {
            "main": [
                IType("beq", "$t1", "test", "$t2"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(100)
        t2.set_contents_from_int(100)
        ProgramStack.jump_label("main")
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)

    def test_beq_false(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        program = {
            "main": [
                IType("beq", "$t1", "test", "$t2"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(100)
        t2.set_contents_from_int(200)
        ProgramStack.jump_label("main")
        next_i = pc.get_contents_as_int() + 4
        ProgramStack.execute_next()
        self.assertEqual(pc.get_contents_as_int(), next_i)

    def test_bne_true(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        program = {
            "main": [
                IType("bne", "$t1", "test", "$t2"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(100)
        t2.set_contents_from_int(200)
        ProgramStack.add_block_from_dict(program)
        ProgramStack.jump_label("main")
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)

    def test_bne_false(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        program = {
            "main": [
                IType("bne", "$t1", "test", "$t2"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(100)
        t2.set_contents_from_int(100)
        ProgramStack.jump_label("main")
        next_i = pc.get_contents_as_int() + 4
        ProgramStack.execute_next()
        self.assertEqual(pc.get_contents_as_int(), next_i)

    def test_blez_true(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        program = {
            "main": [
                IType("blez", "$t1", "test"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(0)
        ProgramStack.jump_label("main")
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)

    def test_blez_false(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        program = {
            "main": [
                IType("blez", "$t1", "test"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(100)
        ProgramStack.jump_label("main")
        next_i = pc.get_contents_as_int() + 4
        ProgramStack.execute_next()
        self.assertEqual(pc.get_contents_as_int(), next_i)

    def test_bgtz_true(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        program = {
            "main": [
                IType("bgtz", "$t1", "test"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(12)
        ProgramStack.jump_label("main")
        ProgramStack.execute_next()
        address = ProgramStack.get_label_addres("test")
        self.assertEqual(pc.get_contents_as_int(), address)

    def test_bgtz_false(self):
        Memory.reset()
        DataHeap.reset()
        ProgramStack.reset()
        pc = RegisterPool.get_register("pc")
        t1 = RegisterPool.get_register("$t1")
        program = {
            "main": [
                IType("bgtz", "$t1", "test"),
                BaseCommand(),
                BaseCommand(),
                BaseCommand(),
            ],
            "test": [BaseCommand()],
        }
        ProgramStack.add_block_from_dict(program)
        t1.set_contents_from_int(-100)
        ProgramStack.jump_label("main")
        next_i = pc.get_contents_as_int() + 4
        ProgramStack.execute_next()
        self.assertEqual(pc.get_contents_as_int(), next_i)

    def test_addi(self):
        i = IType("addi", "$t0", immediate=10, source="$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(10)
        i()
        self.assertEqual(t0.get_contents_as_int(), 20)

    def test_addiu(self):
        i = IType("addiu", "$t0", immediate=-100, source="$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(-1)
        i()
        self.assertEqual(t0.get_contents_as_int(), -101)

    def test_slti(self):
        r = IType("slti", "$t1", 1, "$t2")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t2.set_contents_from_int(2)
        r()
        self.assertEqual(t1.get_contents_as_int(), 0)

    def test_sltiu(self):
        r = IType("sltiu", "$t1", -100, "$t2")
        t1 = RegisterPool.get_register("$t1")
        t2 = RegisterPool.get_register("$t2")
        t2.set_contents_from_int(444)
        r()
        self.assertEqual(t1.get_contents_as_int(), 1)

    def test_andi(self):
        i = IType("andi", "$t0", 79, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(67)
        i()
        self.assertEqual(t0.get_contents_as_int(), 67)

    def test_ori(self):
        i = IType("ori", "$t0", immediate=645, source="$s1")
        t0 = RegisterPool.get_register("$t0")
        s1 = RegisterPool.get_register("$s1")
        s1.set_contents_from_int(123)
        i()
        self.assertEqual(t0.get_contents_as_int(), 767)

    def test_xori(self):
        i = IType("xori", "$t0", immediate=765, source="$s1")
        t0 = RegisterPool.get_register("$t0")
        s1 = RegisterPool.get_register("$s1")
        s1.set_contents_from_int(345)
        i()
        self.assertEqual(t0.get_contents_as_int(), 932)

    def test_lui(self):
        i = IType("lui", "$t1", 0x7777FFFF)
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(0)
        i()
        self.assertEqual(0x00007777, t1.get_contents_as_int())

    def test_lb(self):
        Memory.reset()
        DataStack.alloc(1024)
        i = IType("lb", "$t0", 10, "$t1")
        t0 = RegisterPool.get_register("$t0")
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(123)
        res = Memory.get_byte(123)
        i()
        self.assertEqual(t0.get_contents_as_int(), res)

    def test_lh(self):
        Memory.reset()
        DataStack.store_word(4, 0x11117744)
        i = IType("lh", "$t0", 4, "$sp")
        i()
        t0 = RegisterPool.get_register("$t0")
        self.assertEqual(t0.get_contents_as_int(), 0x7744)

    def test_lw(self):
        # TODO: Not sure if this is correct
        Memory.reset()
        DataStack.alloc(1024)
        DataStack.store_word(4, 1203)
        i = IType("lw", "$t0", 4, source="$sp")
        t0 = RegisterPool.get_register("$t0")
        i()
        self.assertEqual(t0.get_contents_as_int(), 1203)

    def test_lbu(self):
        Memory.reset()
        DataStack.alloc(1024)
        DataStack.store_word(-100, 156)
        i = IType("lbu", "$t0", -100, "$sp")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(0)
        i()
        self.assertEqual(t0.get_contents_as_int(), 156)

    def test_sb(self):
        Memory.reset()
        DataStack.alloc(1024)
        i = IType("sb", "$t0", 10, "$s1")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(37271)
        s1 = RegisterPool.get_register("$s1")
        s1.set_contents_from_int(300)
        i()
        self.assertEqual(Memory.get_word(310), 151)  # Not sure if signed or unsigned

    def test_sh(self):
        Memory.reset()
        DataStack.alloc(1024)
        i = IType("sh", "$t1", 0, ("$sp"))
        t1 = RegisterPool.get_register("$t1")
        t1.set_contents_from_int(0x88884477)
        i()
        res = DataStack.load_word(0, "$sp")
        self.assertEqual(res, 0x4477)

    def test_sw_stack(self):
        Memory.reset()
        # sw $t0, 4($sp)
        DataStack.alloc(1024)
        i = IType("sw", "$t0", 4, "$sp")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(673)
        i()
        self.assertEqual(DataStack.load_word(4, "$sp"), 673)

    def test_sw_heap(self):
        Memory.reset()
        DataHeap.reset()
        DataHeap.alloc(1024)
        DataHeap.store_word(218, "data")
        i = IType("sw", "$t0", "data")
        t0 = RegisterPool.get_register("$t0")
        t0.set_contents_from_int(1999)
        i()
        self.assertEqual(DataHeap.get_value_as_int("data"), 1999)
