"""Data Stack Module

This module houses the DataStack class which is used to replecate MIPS memory access
"""

from PyMIPS.Datastructure.memory import Memory


class Immediate:
    def __init__(self, value):
        self._value = value

    def __call__(self):
        return self._value()

    def __repr__(self):
        return f"Immediate({self()})"


class RefImmediate(Immediate):
    def __call__(self):
        return DataHeap.get_value(self._value)

    def __repr__(self):
        return f"Immediate({self._value}: {self()})"


class Register:
    def __init__(self, name):
        self.name = name
        self.__contents = bytes(0)
        self.__old = bytes(0)

    def __repr__(self):
        return f"Register({self.name}, {str(self.get_contents_as_int())})"

    def set_contents_from_int(self, value: int):
        b = value.to_bytes(5, "big", signed=True)
        self.__contents = b[-4:]
        assert len(self.__contents) == 4
        self.change()

    def set_contents_from_bytes(self, value: bytes):
        if len(value) > 4:
            self.__contents = value[:4]
        else:
            self.__contents = value
        self.change()

    def get_contents_as_int(self):
        return int.from_bytes(self.__contents, "big", signed=True)

    def get_contents_as_unsigned_int(self):
        return int.from_bytes(self.__contents, "big", signed=False)

    def get_contents_as_bytes(self):
        return self.__contents

    def change(self):
        return
        old = int.from_bytes(self.__old, "big")
        new = int.from_bytes(self.__contents, "big")
        print(f"\tRegister {self.name} changed from {old} to {new}")
        self.__old = self.__contents


class RegisterPool:
    """RegisterPool is a collection of static methods that handle register interactions
    """

    __registers = {"$zero": Register("$zero")}

    @staticmethod
    def print_all_active_registers():
        for key in RegisterPool.__registers:
            print(f"\t{RegisterPool.__registers[key]}")

    @staticmethod
    def get_register(name: str) -> Register:
        if name in RegisterPool.__registers.keys():
            return RegisterPool.__registers[name]
        else:
            reg = Register(name)
            RegisterPool.__registers[name] = reg
            return reg


def create_immediate(value) -> Immediate:
    try:
        new = int(value)
        value = new
    except:
        pass
    if type(value) == int:
        return Immediate(lambda: value)
    if type(value) == str:
        return RefImmediate(value)

    return None


def create_register(value) -> Register:
    if value is None:
        return None
    return RegisterPool.get_register(value)


class DataStack:
    __stack_pointer = create_register("$sp")
    __stack_size = 0

    @staticmethod
    def alloc(stack_size: int):
        DataStack.__stack_size = Memory.alloc(stack_size)
        DataStack.__stack_pointer.set_contents_from_int(DataStack.__stack_size)

    @staticmethod
    def store_word(offset: int, value: int, register="$sp"):
        """Replicates the store word functionality of MIPS
        
        Parameters
        ----------
        offset : int
            Offset from the register
        value : int
            The contained value
        register : str, optional
            The register to offset from, by default "$sp"
        """
        # Get the offset register
        r = create_register(register)

        # Calculate the location
        location = r.get_contents_as_int() + offset

        # Set it
        Memory.store_word(value, location)

    @staticmethod
    def load_word(offset: int, register="$sp") -> int:
        """Replicates the load word functionality of mips
        
        Parameters
        ----------
        offset : int
            Offset from register
        register : str, optional
            The register to offset, by default "$sp"
        
        Returns
        -------
        int
            The value stored in the load word as a callable
        """
        # Get the offset register
        r = create_register(register)

        # Calculate the location
        location = r.get_contents_as_int() + offset

        return Memory.get_word(location)


class DataHeap:
    __next_address = 0
    __refs = {}

    @staticmethod
    def reset():
        DataHeap.__next_address = 0
        DataHeap.__refs.clear()

    @staticmethod
    def store_space(label: str, size: int):
        DataHeap.__next_address -= size
        for i in range(size):
            Memory.store_byte(bytes(0), DataHeap.__next_address + i)
        DataHeap.__refs[label] = (DataHeap.__next_address, size)

    @staticmethod
    def alloc(heap_size: int):
        DataHeap.__next_address = Memory.alloc(heap_size)

    @staticmethod
    def store_word(value: int, label: str):
        if label not in DataHeap.__refs.keys():
            DataHeap.__next_address -= 4
            Memory.store_word(value, DataHeap.__next_address)
            DataHeap.__refs[label] = (DataHeap.__next_address, 4)
        else:
            address, _ = DataHeap.__refs[label]
            Memory.store_word(value, address)

    @staticmethod
    def store_asciiz(value: str, label: str):
        if label not in DataHeap.__refs.keys():
            size = len(value) + 1
            size = size + 4 - (size % 4)
            DataHeap.__next_address -= size
            Memory.store_asciiz(value, DataHeap.__next_address)
            DataHeap.__refs[label] = (DataHeap.__next_address, size)
        else:
            address, _ = DataHeap.__refs[label]
            Memory.store_word(value, address)

    @staticmethod
    def get_address(label: str):
        if label in DataHeap.__refs.keys():
            return DataHeap.__refs[label][0]
        raise Exception(f"Heap Address Not Found: {label}")

    @staticmethod
    def get_value(label: str) -> bytes:
        if label not in DataHeap.__refs:
            raise Exception(f"Invalid immediate: {label}")
        address, size = DataHeap.__refs[label]
        b = []
        for i in range(size):
            b.append(Memory.get_byte(address + i))
        return bytes(b)

    @staticmethod
    def get_value_as_int(label: str) -> int:
        b = DataHeap.get_value(label)
        return int.from_bytes(b, "big")

    @staticmethod
    def print():
        print(DataHeap.__refs)


class ProgramStack:
    __labels = {}
    __instructions = {}
    __next_address = 0
    __pc = create_register("pc")

    @staticmethod
    def reset():
        ProgramStack.__labels.clear()
        ProgramStack.__instructions.clear()
        ProgramStack.__next_address = 0
        ProgramStack.__program_counter = 0

    @staticmethod
    def get_label_addres(label: str) -> int:
        if label not in ProgramStack.__labels:
            raise Exception(f"Invalid label {label}")
        return ProgramStack.__labels[label]

    @staticmethod
    def move_pc(amount: int):
        old = ProgramStack.__pc.get_contents_as_int()
        ProgramStack.__pc.set_contents_from_int(old + amount)

    @staticmethod
    def jump_label(label: str):
        if label not in ProgramStack.__labels:
            raise Exception(f"Can't jump to invalid label: {label}")
        ProgramStack.__pc.set_contents_from_int(ProgramStack.__labels[label])

    @staticmethod
    def add_instruction(instruction):
        ProgramStack.__instructions[ProgramStack.__next_address] = instruction
        ProgramStack.__next_address += 4

    @staticmethod
    def execute_instruction(address):
        if address in ProgramStack.__instructions.keys():
            i = ProgramStack.__instructions[address]
            # print(f"{address}: {i}")
            i()
        else:
            raise Exception("Invalid instruction address")

    @staticmethod
    def execute_next():
        next_inst = ProgramStack.__pc.get_contents_as_int()
        ProgramStack.execute_instruction(next_inst)
        if next_inst == ProgramStack.__pc.get_contents_as_int():
            ProgramStack.__pc.set_contents_from_int(next_inst + 4)

    @staticmethod
    def add_label(label):
        name = label.name
        instructions = label.contents
        ProgramStack.__labels[name] = ProgramStack.__next_address
        for i in instructions:
            ProgramStack.add_instruction(i)

    @staticmethod
    def add_text_block(block):
        for l in block.contents:
            ProgramStack.add_label(l)

    @staticmethod
    def add_block_from_dict(block: dict):
        for key in block:
            ProgramStack.__labels[key] = ProgramStack.__next_address
            for inst in block[key]:
                ProgramStack.add_instruction(inst)
