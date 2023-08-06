class Memory:
    __data = {}
    __next_block = 0

    @staticmethod
    def reset():
        Memory.__data.clear()
        Memory.__next_block = 0

    @staticmethod
    def store_byte(value: bytes, address: int):
        old = Memory.get_byte(address)
        Memory.__data[address] = value
        Memory.change(old, value, address)

    @staticmethod
    def change(old: bytes, new: bytes, address: int):
        return
        print(f"\tMemory {address} changed from {old} to {new}")

    @staticmethod
    def get_byte(address: int) -> bytes:
        if address in Memory.__data.keys():
            return Memory.__data[address]
        return 0

    @staticmethod
    def get_word(address: int) -> int:
        b = []
        for i in range(4):
            b.append(Memory.get_byte(address + i))
        return int.from_bytes(b, "big", signed=True)

    @staticmethod
    def store_word(value: int, address: int):
        b = value.to_bytes(4, "big", signed=True)
        for i in range(4):
            Memory.store_byte(b[i], address + i)

    @staticmethod
    def store_ascii(value: str, address: int) -> int:
        b = value.encode("ascii")
        for i in range(len(b)):
            Memory.store_byte(b[i], address + i)
        return len(b)

    @staticmethod
    def store_asciiz(value: str, address: int) -> int:
        value += "\0"
        return Memory.store_ascii(value, address)

    @staticmethod
    def load_asciiz(address: int):
        next_byte = Memory.get_byte(address)
        b = [next_byte]
        address
        i = 1
        while next_byte != 0:
            next_byte = Memory.get_byte(address + i)
            b.append(next_byte)
            i += 1
        data = bytes(b)
        return data.decode("ascii")

    @staticmethod
    def alloc(size: int) -> int:
        Memory.__next_block += size
        return Memory.__next_block

    @staticmethod
    def print():
        addresses = list(Memory.__data.keys())
        addresses.sort()
        for key in addresses:
            block = Memory.get_byte(key)
            print(f"{key}: 0x{block}")

