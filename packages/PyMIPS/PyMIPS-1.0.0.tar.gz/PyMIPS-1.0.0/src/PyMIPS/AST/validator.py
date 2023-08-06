def validate(instruction) -> bool:
    """Validates an instruction
    
    Parameters
    ----------
    instruction : BaseCommand
        The instruction to validate
    
    Returns
    -------
    bool
        Valid or not valid
    """
    switch = {
        # R Type instructions
        "add": validate_3_rtype,
        "addu": validate_3_rtype,
        "and": validate_3_rtype,
        "nor": validate_3_rtype,
        "or": validate_3_rtype,
        "sll": validate_2_itype,
        "sllv": validate_3_rtype,
        "slt": validate_3_rtype,
        "sltu": validate_3_rtype,
        "sra": validate_2_itype,
        "srav": validate_3_rtype,
        "srl": validate_2_itype,
        "srlv": validate_3_rtype,
        "sub": validate_3_rtype,
        "subu": validate_3_rtype,
        "xor": validate_3_rtype,
        "div": validate_2_rtype,
        "divu": validate_2_rtype,
        "jalr": validate_jalr,
        "mul": validate_2_rtype,
        "mult": validate_2_rtype,
        "madd": validate_2_rtype,
        "maddu": validate_2_rtype,
        "msub": validate_2_rtype,
        "msubu": validate_2_rtype,
        "move": validate_2_rtype,
        "not": validate_2_rtype,
        "teq": validate_2_rtype,
        "tge": validate_2_rtype,
        "tgeu": validate_2_rtype,
        "tlt": validate_2_rtype,
        "tltu": validate_2_rtype,
        "tne": validate_2_rtype,
        "jr": validate_1_rtype,
        "mfhi": validate_1_rtype,
        "mflo": validate_1_rtype,
        "mthi": validate_1_rtype,
        "mtlo": validate_1_rtype,
        "syscall": validate_0_rtype,
        "eret": validate_0_rtype,
        "nop": validate_0_rtype,
        # I Type instructions
        "addi": validate_2_itype,
        "addiu": validate_2_itype,
        "andi": validate_2_itype,
        "beq": validate_2_itype,
        "bne": validate_2_itype,
        "ori": validate_2_itype,
        "slti": validate_2_itype,
        "sltiu": validate_2_itype,
        "xori": validate_2_itype,
        "li": validate_1_itype,
        "la": validate_optional_2_itype,
        "bgezal": validate_1_itype,
        "beqz": validate_1_itype,
        "bgez": validate_1_itype,
        "bgtz": validate_1_itype,
        "blez": validate_1_itype,
        "bltz": validate_1_itype,
        "bnez": validate_1_itype,
        "lui": validate_1_itype,
        "tgei": validate_1_itype,
        "teqi": validate_1_itype,
        "tgeiu": validate_1_itype,
        "tlti": validate_1_itype,
        "tltiu": validate_1_itype,
        "tnei": validate_1_itype,
        "bge": validate_optional_2_itype,
        "sw": validate_optional_2_itype,
        "sc": validate_optional_2_itype,
        "swl": validate_optional_2_itype,
        "lw": validate_optional_2_itype,
        "ll": validate_optional_2_itype,
        "lb": validate_optional_2_itype,
        "lbu": validate_optional_2_itype,
        "lh": validate_optional_2_itype,
        "lhu": validate_optional_2_itype,
        "sb": validate_optional_2_itype,
        "sh": validate_optional_2_itype,
        # J-Type Instructions
        "j": validate_jtype,
        "jal": validate_jtype,
    }
    try:
        func = switch[instruction.command]
        res = func(instruction)
    except KeyError:
        res = True
        print(f"Validation for {instruction.command} not implemented")
    except:
        res = False
    return res


list_of_registers = (
    "$zero",
    "$v0",
    "$v1",
    "$a0",
    "$a1",
    "$a2",
    "$a3",
    "$t0",
    "$t1",
    "$t2",
    "$t3",
    "$t4",
    "$t5",
    "$t6",
    "$t7",
    "$s0",
    "$s1",
    "$s2",
    "$s3",
    "$s4",
    "$s5",
    "$s6",
    "$s7",
    "$t8",
    "$t9",
    "$sp",
    "$ra",
)


def validate_jalr(inst):
    return validate_1_rtype(inst) or validate_2_rtype(inst)


def validate_3_rtype(instruction) -> bool:
    """Validates R-Type instructions with 3 registers 
    
    Parameters
    ----------
    instruction : R-Type
        R-types with 3 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    rd = instruction.destination_register
    rs = instruction.source_register
    rt = instruction.target_register

    check1 = rd is not None
    check2 = rs is not None
    check3 = rt is not None

    if (
        rd.name in list_of_registers
        and rs.name in list_of_registers
        and rt.name in list_of_registers
    ):
        return check1 and check2 and check3
    return False


def validate_2_rtype(instruction) -> bool:
    """Validates R-Type instructions with 2 registers 
    
    Parameters
    ----------
    instruction : R-Type
        R-types with 2 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    rd = instruction.destination_register
    rs = instruction.source_register
    rt = instruction.target_register

    check1 = rd is not None
    check2 = rs is not None
    check3 = rt is None

    if rd.name in list_of_registers and rs.name in list_of_registers:
        return check1 and check2 and check3
    return False


def validate_1_rtype(instruction) -> bool:
    """Validates R-Type instructions with 1 registers 
    
    Parameters
    ----------
    instruction : R-Type
        R-types with 1 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    rd = instruction.destination_register
    rs = instruction.source_register
    rt = instruction.target_register

    check1 = rd is not None
    check2 = rs is None
    check3 = rt is None

    if rd.name in list_of_registers:
        return check1 and check2 and check3
    return False


def validate_0_rtype(instruction) -> bool:
    """Validates R-Type instructions with 0 registers 
    
    Parameters
    ----------
    instruction : R-Type
        R-types with 0 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    rd = instruction.destination_register
    rs = instruction.source_register
    rt = instruction.target_register

    check1 = rd is None
    check2 = rs is None
    check3 = rt is None

    return check1 and check2 and check3


def validate_2_itype(instruction) -> bool:
    """Validates I-Type instructions with 2 registers 
    
    Parameters
    ----------
    instruction : I-Type
        I-types with 2 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    destination = instruction.destination_register
    source = instruction.source_register
    immediate = instruction.immediate

    check1 = destination is not None
    check2 = source is not None
    check3 = immediate is not None
    if instruction.command in ("beq", "bne", "sll", "srl", "sra") and isinstance(
        immediate._value, str
    ):
        if destination.name in list_of_registers and source.name in list_of_registers:
            return check1 and check2 and check3
    elif (
        destination.name in list_of_registers
        and isinstance(immediate(), int)
        and source.name in list_of_registers
    ):
        return check1 and check2 and check3
    return False


def validate_optional_2_itype(instruction) -> bool:
    """Validates I-Type instructions with optional 2 registers 
    
    Parameters
    ----------
    instruction : I-Type
        I-types with 2 optional registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    destination = instruction.destination_register
    target = instruction.target_register
    source = instruction.source_register
    immediate = instruction.immediate

    check1 = destination is not None
    check2 = immediate is not None
    check3 = target is None

    if destination.name in list_of_registers:
        if source is not None and source.name in list_of_registers:
            return check1 and check2 and check3
        elif source is None:
            return check1 and check2 and check3
    return False


def validate_1_itype(instruction) -> bool:
    """Validates I-Type instructions with 1 registers 
    
    Parameters
    ----------
    instruction : I-Type
        I-types with 1 registers
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    destination = instruction.destination_register
    target = instruction.target_register
    immediate = instruction.immediate
    source = instruction.source_register

    check1 = destination is not None
    check2 = target is None
    check3 = immediate is not None
    check4 = source is None

    if destination.name in list_of_registers:
        return check1 and check2 and check3 and check4
    return False


def validate_jtype(instruction) -> bool:
    """Validates J-Type instructions
    
    Parameters
    ----------
    instruction : J-Type
        
    
    Returns
    -------
    bool
        [Syntax correct or not]
    """
    address = instruction.address
    check = address is not None

    return check

