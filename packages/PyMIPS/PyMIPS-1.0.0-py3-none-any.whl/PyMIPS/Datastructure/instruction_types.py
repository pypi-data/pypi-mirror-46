from PyMIPS.Datastructure.commands import get_command
from PyMIPS.Datastructure.data_model import create_register, create_immediate
from PyMIPS.AST.validator import validate


class BaseCommand:
    def __init__(self, command_str="BASE"):
        """Base Command Class
        move $dest, $source
        add $dest, $source, $targ
        li $dest, immediate
        """
        self.command = None
        self.destination_register = None  # The register to be mutated
        self.source_register = None  # The source register
        self.target_register = None  # The second source register
        self.shamt = None  # Shift amount
        self.immediate = None  # Immediate
        self.address = None  # Address for J Types
        self.func = lambda: False
        self.command_string = command_str

    def __call__(self):
        return self.func()

    def __repr__(self):
        return self.command_string


class IType(BaseCommand):
    def __init__(
        self,
        command: str,
        destination: str,
        immediate,
        source: str = None,
        command_str="",
    ):
        """Stores I_Type commands
        
        Parameters
        ----------
        command : str
            An I_Type command string
        destination : str
            Name of destination register
        immediate : any
            An immediate (See immediate for details)
        source : str, optional
            Name of source register, by default None
        """
        super().__init__(command_str)
        self.command = command
        self.destination_register = create_register(destination)
        self.source_register = create_register(source)
        self.immediate = create_immediate(immediate)
        if not validate(self):
            raise Exception("Seg Fault :p")
        self.func = get_command(self)


class RType(BaseCommand):
    def __init__(
        self,
        command: str,
        destination: str,
        source_register: str = None,
        target_register: str = None,
        shamt: int = 0,
        command_str="",
    ):
        """Stores R_Type commands
        
        Parameters
        ----------
        command : str
            R Type command string
        destination_register : str
            Destination register name
        source_register : str, optional
            Source register name, by default None
        target_register : str, optional
            Target register name, by default None
        shamt : int, optional
            Shift amount, by default 0
        """
        super().__init__(command_str)
        self.command = command
        self.destination_register = create_register(destination)
        self.source_register = create_register(source_register)
        self.target_register = create_register(target_register)
        self.shamt = shamt
        if not validate(self):
            raise Exception("Seg Fault :p")
        self.func = get_command(self)


class JType(BaseCommand):
    def __init__(self, command: str, address, command_str=""):
        """Stores J Type commands
        
        Parameters
        ----------
        command : str
            J type command string
        address : not sure yet
            TODO
        """
        super().__init__(command_str)
        self.command = command
        self.address = address
        if not validate(self):
            raise Exception("Seg Fault :p")
        self.func = get_command(self)


def unpack(contents) -> list:
    # Check to see if tuple
    if type(contents) != tuple:
        return [contents]
    result = []
    while type(contents) == tuple:
        value, contents = contents
        if type(value) == tuple:
            value, contents = contents, value

        result.append(value)
    result.append(contents)
    return result

