import sys, os
from vm import Parser, CodeWriter, CommandType

def main():

    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        # ディレクトリの場合
        vm_files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.vm')]
        output_path = os.path.join(input_path, os.path.basename(input_path) + '.asm')
        code_writer = CodeWriter(output_path)
        code_writer.write_init()  # ブートストラップコード
        for vm_file in vm_files:
            filename = os.path.basename(vm_file).replace('.vm', '')
            parser = Parser(vm_file)
            code_writer.set_file_name(filename)
            while parser.has_more_commands():
                parser.advance()
                command_type = parser.command_type()
                if command_type == CommandType.C_ARITHMETIC:
                    code_writer.write_arithmetic(parser.arg1())
                elif command_type in (CommandType.C_PUSH, CommandType.C_POP):
                    code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
                elif command_type == CommandType.C_LABEL:
                    code_writer.write_label(parser.arg1())
                elif command_type == CommandType.C_GOTO:
                    code_writer.write_goto(parser.arg1())
                elif command_type == CommandType.C_IF:
                    code_writer.write_if(parser.arg1())
                elif command_type == CommandType.C_CALL:
                    code_writer.write_call(parser.arg1(), parser.arg2())
                elif command_type == CommandType.C_RETURN:
                    code_writer.write_return()
                elif command_type == CommandType.C_FUNCTION:
                    code_writer.write_function(parser.arg1(), parser.arg2())
                else:
                    raise ValueError(f"Unknown command type: {command_type}")
        code_writer.close()
    else:
        # ファイルの場合
        output_path = input_path.replace('.vm', '.asm')
        filename = os.path.basename(input_path).replace('.vm', '')
        parser = Parser(input_path)
        code_writer = CodeWriter(output_path)
        code_writer.write_init()  # ブートストラップコード
        code_writer.set_file_name(filename)
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == CommandType.C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif command_type in (CommandType.C_PUSH, CommandType.C_POP):
                code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
            elif command_type == CommandType.C_LABEL:
                code_writer.write_label(parser.arg1())
            elif command_type == CommandType.C_GOTO:
                code_writer.write_goto(parser.arg1())
            elif command_type == CommandType.C_IF:
                code_writer.write_if(parser.arg1())
            elif command_type == CommandType.C_CALL:
                code_writer.write_call(parser.arg1(), parser.arg2())
            elif command_type == CommandType.C_RETURN:
                code_writer.write_return()
            elif command_type == CommandType.C_FUNCTION:
                code_writer.write_function(parser.arg1(), parser.arg2())
            else:
                raise ValueError(f"Unknown command type: {command_type}")
        code_writer.close()

if __name__ == "__main__":
    main()