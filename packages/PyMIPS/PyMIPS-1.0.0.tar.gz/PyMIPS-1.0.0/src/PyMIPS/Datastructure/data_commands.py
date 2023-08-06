from PyMIPS.Datastructure.data_model import DataHeap
import json


class DataWord:
    def __init__(self, data: tuple):
        ((self.label, _), self.value) = data

    def __repr__(self):
        return f"Word({self.label} {self.value})"

    def __call__(self):
        DataHeap.store_word(int(self.value), self.label[:-1])


class DataAsciiz:
    def __init__(self, data: tuple):
        ((self.label, _), self.value) = data

    def __repr__(self):
        return f"Asciiz({self.label} {self.value})"

    def __call__(self):
        DataHeap.store_asciiz(json.loads(self.value), self.label[:-1])


class DataSpace:
    def __init__(self, data: tuple):
        ((self.label, _), self.value) = data

    def __repr__(self):
        return f"Space({self.label} size {self.value})"

    def __call__(self):
        DataHeap.store_space(self.label[:-1], int(self.value))
