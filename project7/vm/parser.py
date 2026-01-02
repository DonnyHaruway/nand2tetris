from .constants import CommandType

class Parser:
    def __init__(self, input_file : str):
        self.file = open(input_file, 'r')
        self.current_command = None
        self.lines = self.file.readlines()
        self.current_index = -1

    def has_more_commands(self) -> bool:
        return self.current_index + 1 < len(self.lines)
    
    def advance(self):
        if self.has_more_commands():
            self.current_index += 1
            line = self.lines[self.current_index]
            line = line.split('//')[0].strip()  # Remove comments and whitespace
            if line:
                self.current_command = line
            else:
                self.advance()  # Skip empty lines
        else:
            self.current_command = None

    def command_type(self) -> str:
        if self.current_command is None:
            return None
        parts = self.current_command.split()
        cmd = parts[0]
        if cmd in {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}:
            return CommandType.C_ARITHMETIC
        elif cmd == 'push':
            return CommandType.C_PUSH
        elif cmd == 'pop':
            return CommandType.C_POP
        elif cmd == 'label':
            return CommandType.C_LABEL
        elif cmd == 'goto':
            return CommandType.C_GOTO
        elif cmd == 'if-goto':
            return CommandType.C_IF
        elif cmd == 'function':
            return CommandType.C_FUNCTION
        elif cmd == 'return':
            return CommandType.C_RETURN
        elif cmd == 'call':
            return CommandType.C_CALL
        else:
            return None
        
    def arg1(self) -> str:
        if self.current_command is None:
            return None
        cmd_type = self.command_type()
        parts = self.current_command.split()
        if cmd_type == CommandType.C_ARITHMETIC:
            return parts[0]
        elif cmd_type in {
                CommandType.C_PUSH, CommandType.C_POP,
                CommandType.C_LABEL, CommandType.C_GOTO,
                CommandType.C_IF, CommandType.C_FUNCTION,
                CommandType.C_CALL
            }:
            return parts[1]
        else:
            return None
        
    def arg2(self) -> int:
        if self.current_command is None:
            return None
        cmd_type = self.command_type()
        parts = self.current_command.split()
        if cmd_type in {
                CommandType.C_PUSH, CommandType.C_POP,
                CommandType.C_FUNCTION, CommandType.C_CALL
            }:
            return int(parts[2])
        else:
            return None