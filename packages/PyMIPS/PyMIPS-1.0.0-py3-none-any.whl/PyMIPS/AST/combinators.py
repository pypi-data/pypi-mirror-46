class Result:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"({self.value})"


class Parser:
    def __call__(self, tokens, pos):
        pass

    def __add__(self, other):
        return Combinator(self, other)

    def __xor__(self, func):
        return Processor(self, func)

    def __or__(self, other):
        return Alternator(self, other)


class Combinator(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_res = self.left(tokens, pos)
        if left_res:
            right_res = self.right(tokens, left_res.pos)
            if right_res:
                comb = (left_res.value, right_res.value)
                return Result(comb, right_res.pos)
        return None


class Alternator(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_res = self.left(tokens, pos)
        if left_res:
            return left_res
        else:
            return self.right(tokens, pos)


class Lazy(Parser):
    def __init__(self, generator):
        self.parser = None
        self.generator = generator

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.generator()
        return self.parser(tokens, pos)


class Processor(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.func(result.value)
            return result


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        return None


class Keyword(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if (
            pos < len(tokens)
            and self.value == tokens[pos][0]
            and self.tag is tokens[pos][1]
        ):
            return Result(tokens[pos][0], pos + 1)
        return None
