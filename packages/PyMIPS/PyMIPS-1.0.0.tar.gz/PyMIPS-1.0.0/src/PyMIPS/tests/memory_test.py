try:
    from src.PyMIPS.Datastructure.memory import Memory
except:
    from PyMIPS.Datastructure.memory import Memory

import unittest


class TestMemory(unittest.TestCase):
    def test_storage(self):
        Memory.store_word(16, 2214)
        Memory.store_word(17, 2014)

        self.assertEqual(Memory.get_word(2214), 16)
        self.assertEqual(Memory.get_word(2014), 17)

    def test_bad_access(self):
        Memory.store_word(16, 2000)

        Memory.get_word(2004)
        Memory.get_word(2001)
        Memory.get_word(2002)
        Memory.get_word(2003)

    def test_overwrite(self):
        Memory.store_word(16, 2000)
        self.assertEqual(Memory.get_word(2000), 16)

        Memory.store_word(20, 2001)
        self.assertEqual(Memory.get_word(2001), 20)

        self.assertEqual(Memory.get_word(2000), 0)
