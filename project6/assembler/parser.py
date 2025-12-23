class Parser: 
    def __init__(self, commands : list[str]):
        self.commands = commands
        self.cur = 0
    
    def has_more_commands(self) -> bool:
        return self.cur < len(self.commands)
    
    def advance(self) -> None:
        if self.has_more_commands():
            self.cur += 1
        else:
            raise IndexError("No more commands to advance to.")
    
    def command_type(self) -> str:
        current_command = self.commands[self.cur]
        if current_command.startswith('@'):
            return 'A_COMMAND'
        elif current_command.startswith('(') and current_command.endswith(')'):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'
        
    def symbol(self) -> str:
        current_command = self.commands[self.cur]
        cmd_type = self.command_type()
        
        if cmd_type == 'A_COMMAND':
            return current_command[1:]
        elif cmd_type == 'L_COMMAND':
            return current_command[1:-1]
        else:
            raise ValueError("Current command is not A_COMMAND or L_COMMAND.")

    def dest(self) -> str:
        current_command = self.commands[self.cur]
        if self.command_type() != 'C_COMMAND':
            raise ValueError("Current command is not C_COMMAND.")
        
        if '=' in current_command:
            return current_command.split('=')[0]
        else:
            return 'null'
        
    def comp(self) -> str:
        current_command = self.commands[self.cur]
        if self.command_type() != 'C_COMMAND':
            raise ValueError("Current command is not C_COMMAND.")
        
        if '=' in current_command:
            return current_command.split('=')[1]
        else:
            return current_command.split(';')[0]

    def jump(self) -> str:
        current_command = self.commands[self.cur]
        if self.command_type() != 'C_COMMAND':
            raise ValueError("Current command is not C_COMMAND.")
        
        if ';' in current_command:
            return current_command.split(';')[1]
        else:
            return 'null'