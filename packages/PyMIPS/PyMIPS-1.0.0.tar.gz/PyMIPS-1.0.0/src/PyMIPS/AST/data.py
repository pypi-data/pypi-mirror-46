class WordDeclaration:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"{self.name} {self.size}"


class Asciiz:
    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def __repr__(self):
        return f"{self.name} {self.contents}"
