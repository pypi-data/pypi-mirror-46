from PyMIPS.Datastructure.data_model import ProgramStack


class Globl:
    def __init__(self, entry):
        self.entry = entry

    def __repr__(self):
        return f"Entry Point: {self.entry}\n"

    def __call__(self):
        ProgramStack.jump_label(self.entry)


class TextBlock:
    def __init__(self, contents):
        self.contents = unpack(contents)
        self.globl = None
        for c in self.contents:
            if type(c) == Globl:
                self.globl = c
                self.contents.remove(c)
                break

    def __repr__(self):
        c = ""
        for item in self.contents:
            c += str(item) + "\n"

        return f"Text Block:\n{c}"

    def get_globl(self):
        return self.globl


class DataBlock:
    def __init__(self, contents):
        self.contents = unpack(contents)

    def __repr__(self):
        c = ""
        for item in self.contents:
            c += "\t" + str(item) + "\n"
        return f"Data Block:\n{c}"

    def __call__(self):
        for c in self.contents:
            c()


class Label:
    def __init__(self, name, contents):
        self.name = name[:-1]
        self.contents = unpack(contents)

    def __repr__(self):
        c = ""
        for item in self.contents:
            c += "\t" + str(item) + "\n"
        return f"{self.name}\n{str(c)}"


class Program:
    def __init__(self, contents):
        self.contents = unpack(contents)
        self.data = None
        self.text = None
        self.globl = None
        self.link()

    def link(self):
        for c in self.contents:
            if type(c) == DataBlock and self.data is None:
                self.data = c
            elif type(c) == TextBlock and self.text is None:
                self.text = c
            elif type(c) == Globl and self.globl is None:
                self.globl = c
            else:
                raise Exception("Invalid block")

        if self.text is None:
            raise Exception("No text block")

        if self.data is None:
            self.data = lambda: 0

        text_globl = self.text.get_globl()
        if text_globl and self.globl is None:
            self.globl = text_globl
        elif text_globl:
            raise Exception("Too many .globl directives")
        if self.globl is None:
            self.globl = Globl("main")

    def __repr__(self):
        c = ""
        for item in self.contents:
            c += str(item)
        return f"Program:\n\n{c}"


def unpack(contents: tuple) -> list:
    result = []
    while type(contents) == tuple:
        value, contents = contents
        result.append(value)
    result.append(contents)
    return result

