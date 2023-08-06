from PyMIPS.Datastructure.instruction_types import RType, JType, IType


def create_i_type(package: tuple) -> IType:

    u = unpack_sequential(package)
    c_string = " ".join(u)

    def r_1(tokens: list):
        return IType(tokens[0], tokens[1], tokens[3], command_str=c_string)

    def r_2(tokens: list):
        return IType(tokens[0], tokens[1], tokens[5], tokens[3], command_str=c_string)

    def offset(tokens: list):
        return IType(tokens[0], tokens[1], tokens[3], tokens[5], command_str=c_string)

    return {4: r_1, 6: r_2, 7: offset}[len(u)](u)


def create_r_type(package: tuple) -> RType:
    u = unpack_sequential(package)
    c_string = " ".join(u)

    def r_3(tokens: list):
        return RType(tokens[0], tokens[1], tokens[3], tokens[5], command_str=c_string)

    def r_2(tokens: list):
        return RType(tokens[0], tokens[1], tokens[3], command_str=c_string)

    def r_1(tokens: list):
        return RType(tokens[0], tokens[1], command_str=c_string)

    return {6: r_3, 4: r_2, 2: r_1}[len(u)](u)


def create_j_type(package: tuple) -> JType:
    u = unpack_sequential(package)
    c_string = " ".join(u)
    return JType(u[0], u[1], command_str=c_string)


def create_syscall() -> RType:
    return RType("syscall", None, command_str="syscall")


def unpack_sequential(package: tuple) -> list:
    front = []
    back = []
    while type(package) == tuple:
        left, right = package
        if type(right) != tuple:
            back.append(right)
            package = left
        if type(left) != tuple:
            front.append(left)
            package = right
    back.reverse()
    return front + back
