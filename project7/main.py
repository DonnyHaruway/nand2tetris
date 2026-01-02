import sys, os
from vm import Parser, CodeWriter, CommandType

def main():

    input_path = sys.argv[1]
    output_path = input_path.replace('.vm', '.asm')
    filename = os.path.basename(input_path).replace('.vm', '')

    parser = Parser(input_path)

    code_writer = CodeWriter(output_path)
    code_writer.set_file_name(filename)

    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()

        if command_type == CommandType.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif command_type in (CommandType.C_PUSH, CommandType.C_POP):
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
        # Handle other command types as needed

    code_writer.close()

if __name__ == "__main__":
    main()