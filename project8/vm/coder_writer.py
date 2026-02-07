from .constants import CommandType
class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.file = open(output_file, 'w')
        self.label_counter = 0

    def write_init(self):
        asm = [
            "@256", 
            "D=A",
            "@SP",
            "M=D" # Initialize SP=256
        ]
        self.file.write("\n".join(asm) + "\n")
        self.write_call("Sys.init", 0)

    def set_file_name(self, filename: str):
        self.current_filename = filename

    def write_arithmetic(self, command: str):
        if command == 'add':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=D+M"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == 'sub':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=M-D"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == 'neg':
            asm = [
                "@SP",
                "A=M-1",
                "M=-M"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == 'eq':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{self.current_filename}.EQ_TRUE.{self.label_counter}",
                "D;JEQ",
                "@SP",
                "A=M-1",
                "M=0", # false
                f"@{self.current_filename}.EQ_END.{self.label_counter}",
                "0;JMP",
                f"({self.current_filename}.EQ_TRUE.{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"({self.current_filename}.EQ_END.{self.label_counter})"
            ]
            self.file.write("\n".join(asm) + "\n")
            self.label_counter += 1
        elif command == 'gt':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{self.current_filename}.GT_TRUE.{self.label_counter}",
                "D;JGT",
                "@SP",
                "A=M-1",
                "M=0",  # false
                f"@{self.current_filename}.GT_END.{self.label_counter}",
                "0;JMP",
                f"({self.current_filename}.GT_TRUE.{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"({self.current_filename}.GT_END.{self.label_counter})"
            ]
            self.file.write("\n".join(asm) + "\n")
            self.label_counter += 1

        elif command == 'lt':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{self.current_filename}.LT_TRUE.{self.label_counter}",
                "D;JLT",
                "@SP",
                "A=M-1",
                "M=0",  # false
                f"@{self.current_filename}.LT_END.{self.label_counter}",
                "0;JMP",
                f"({self.current_filename}.LT_TRUE.{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"({self.current_filename}.LT_END.{self.label_counter})"
            ]
            self.file.write("\n".join(asm) + "\n")
            self.label_counter += 1
        elif command == 'and':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=M&D"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == 'or':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=M|D"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == 'not':
            asm = [
                "@SP",
                "A=M-1",
                "M=!M"
            ]
            self.file.write("\n".join(asm) + "\n")
        else:
            raise ValueError(f"Unknown arithmetic command: {command}")

    def write_push_pop(self, command: str, segment: str, index: int):
        if command == CommandType.C_PUSH:
            if segment == 'argument':
                asm = [
                    "@ARG",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                ]
            elif segment == 'local':
                asm = [
                    "@LCL",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                ]
            elif segment == 'static':
                asm = [
                    f"@{self.current_filename}.{index}",
                    "D=M",
                ]
            elif segment == 'constant':
                asm = [
                    f"@{index}",
                    "D=A",
                ]
            elif segment == 'this':
                asm = [
                    "@THIS",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                ]
            elif segment == 'that':
                asm = [
                    "@THAT",
                    "D=M",
                    f"@{index}",
                    "A=D+A",
                    "D=M",
                ]
            elif segment == 'pointer':
                asm = [
                    f"@{3 + index}",
                    "D=M",
                ]
            elif segment == 'temp':
                asm = [
                    f"@{5 + index}",
                    "D=M",
                ]
            else:
                raise ValueError(f"Unknown segment: {segment}")
            asm += [
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
            self.file.write("\n".join(asm) + "\n")
        elif command == CommandType.C_POP:
            if segment in ['local', 'argument', 'this', 'that']:
                seg_map = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
                asm = [
                    f"@{seg_map[segment]}",
                    "D=M",
                    f"@{index}",
                    "D=D+A",
                    "@R13",
                    "M=D"
                ]
            elif segment == 'temp':
                asm = [
                    f"@{5 + index}",
                    "D=A",
                    "@R13",
                    "M=D"
                ]
            elif segment == 'pointer':
                target = "THIS" if index == 0 else "THAT"
                asm = [
                    f"@{target}",
                    "D=A",
                    "@R13",
                    "M=D"
                ]
            elif segment == 'static':
                asm = [
                    f"@{self.current_filename}.{index}",
                    "D=A",
                    "@R13",
                    "M=D"
                ]
            else:
                raise ValueError(f"Unknown segment: {segment}")
            asm += [
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]
            self.file.write("\n".join(asm) + "\n")
        else:
            raise ValueError(f"Unknown command type: {command}")

    def write_label(self, label: str):
        asm = [
            f"({label})"
        ]
        self.file.write("\n".join(asm) + "\n")

    def write_goto(self, label: str):
        asm = [
            f"@{label}",
            "0;JMP"
        ]
        self.file.write("\n".join(asm) + "\n")

    def write_if(self, label: str):
        asm = [
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{label}",
            "D;JNE"
        ]
        self.file.write("\n".join(asm) + "\n")

    def write_call(self, function_name: str, num_args: int):
        asm = [
            f"@RETURN_ADDRESS{self.label_counter}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "@LCL",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "@ARG",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "@THIS",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "@THAT",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            "@SP",
            "D=M",
            f"@{num_args + 5}",
            "D=D-A",
            "@ARG",
            "M=D",
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            f"@{function_name}",
            "0;JMP",
            f"(RETURN_ADDRESS{self.label_counter})"
        ]

        self.file.write("\n".join(asm) + "\n")
        self.label_counter += 1

    def write_return(self):
        asm = [
            "@LCL",
            "D=M",
            "@R13", # Memory[R13] = FRAME
            "M=D",
            "@5",
            "A=D-A",
            "D=M",
            "@R14", # Memory[R14] = RET
            "M=D",  # RET = *(FRAME-5)
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",  # *ARG = pop()
            "@ARG",
            "D=M+1",  
            "@SP",
            "M=D",  # SP = ARG + 1
            "@R13",
            "AM=M-1",
            "D=M",  
            "@THAT",
            "M=D",  # THAT = *(FRAME-1)
            "@R13",
            "AM=M-1",
            "D=M",
            "@THIS",
            "M=D",  # THIS = *(FRAME-2)
            "@R13",
            "AM=M-1",
            "D=M",
            "@ARG",
            "M=D",  # ARG = *(FRAME-3)
            "@R13",
            "AM=M-1",
            "D=M",
            "@LCL",
            "M=D",  # LCL = *(FRAME-4)
            "@R14",
            "A=M",
            "0;JMP" # goto RET
        ]
        self.file.write("\n".join(asm) + "\n")

    def write_function(self, function_name: str, num_locals: int):
        asm = [
            f"({function_name})"
        ]
        for _ in range(num_locals):
            asm += [
                "@0",
                "D=A",
                "@SP",
                "A=M",
                "M=D",  # push 0 onto the stack
                "@SP",
                "M=M+1" # SP++
            ]
        self.file.write("\n".join(asm) + "\n")

    def close(self):
        self.file.close()
        # 末尾の改行を削除
        with open(self.output_file, 'rb+') as f:
            f.seek(0, 2)  # ファイルの末尾へ
            filesize = f.tell()
            if filesize == 0:
                return
            f.seek(-1, 2)
            last_char = f.read(1)
            if last_char == b'\n':
                f.truncate(filesize - 1)