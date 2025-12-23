import re
import os
from parser import Parser
from code import Code
from symbol_table import SymbolTable

def load_and_process(file_path : str) -> list[str]:
    """
    road the assembly file and process its content.
    """
    cleaned_commands = []
    with open(file_path, 'r') as f:
        for line in f:
            comment_removed_line = re.sub(r'//.*', '', line)
            completely_stripped_line = re.sub(r'\s', '', comment_removed_line)

            if completely_stripped_line:
                cleaned_commands.append(completely_stripped_line)
    
    return cleaned_commands

def first_pass(commands: list[str], symbol_table: SymbolTable) -> None:
    """
    First pass to add label symbols to the symbol table.
    """
    rom_address = 0
    parser = Parser(commands)
    
    while parser.has_more_commands():
        cmd_type = parser.command_type()
        
        if cmd_type == 'L_COMMAND':
            symbol = parser.symbol()
            if not symbol_table.contains(symbol):
                symbol_table.add_entry(symbol, rom_address)
        else:
            rom_address += 1
        
        parser.advance()

def second_pass(commands: list[str], symbol_table: SymbolTable) -> list[str]:
    """
    Second pass to add variable symbols to the symbol table.
    """
    parser = Parser(commands)
    code = Code()
    binary_strings = []
    while parser.has_more_commands():
        cmd_type = parser.command_type()
        
        if cmd_type == 'A_COMMAND':
            symbol = parser.symbol()
            if not symbol.isdigit():
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, symbol_table.next_variable_address)
                    symbol_table.next_variable_address += 1
                address = symbol_table.get_address(symbol)
                binary_strings.append(f"0{address:015b}")
            else:
                address = int(symbol)
                binary_strings.append(f"0{address:015b}")

        elif cmd_type == 'C_COMMAND':
            dest_mnemonic = parser.dest()
            comp_mnemonic = parser.comp()
            jump_mnemonic = parser.jump()
            
            dest_bits = code.dest(dest_mnemonic)
            comp_bits = code.comp(comp_mnemonic)
            jump_bits = code.jump(jump_mnemonic)
            binary_strings.append(f"111{comp_bits}{dest_bits}{jump_bits}")

        elif cmd_type == 'L_COMMAND':
            symbol = parser.symbol()
        
        parser.advance()
    return binary_strings

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '../RectL.asm')
    commands = load_and_process(file_path)

    symbol_table = SymbolTable()
    first_pass(commands, symbol_table)
    binary_strings = second_pass(commands, symbol_table)

    output_path = os.path.join(script_dir, '../RectL.hack')
    with open(output_path, 'w') as f:
        f.write('\n'.join(binary_strings))

if __name__ == "__main__":
    main()