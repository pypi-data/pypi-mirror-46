try:
    from src.PyMIPS.Datastructure.memory import Memory
    from src.PyMIPS.Datastructure.data_model import DataStack, DataHeap
except:
    from PyMIPS.Datastructure.memory import Memory
    from PyMIPS.Datastructure.data_model import DataStack, DataHeap

import unittest


class TestDataStack(unittest.TestCase):
    def test_storage(self):
        DataStack.alloc(255)
        DataStack.store_word(4, 16)
        self.assertEqual(DataStack.load_word(4), 16)


class TestDataHeap(unittest.TestCase):
    def test_storage(self):
        DataHeap.alloc(255)
        DataHeap.store_word(118, "V")
        self.assertEqual(DataHeap.get_value_as_int("V"), 118)
        DataHeap.store_word(119, "V")
        self.assertEqual(DataHeap.get_value_as_int("V"), 119)

