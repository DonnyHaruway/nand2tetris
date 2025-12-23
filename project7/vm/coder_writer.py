class CodeWriter:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.file = open(output_file, 'w')
        self.label_counter = 0

    def set_file_name(self, filename: str):
        self.current_filename = filename

    def write_arithmetic(self, command: str):
        if command == 'add':
            asm = [
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "M=M+D"
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
                f"@EQ_TRUE{self.label_counter}",
                "D;JEQ",
                "@SP",
                "A=M-1",
                "M=0",  # false
                f"@EQ_END{self.label_counter}",
                "0;JMP",
                f"(EQ_TRUE{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"(EQ_END{self.label_counter})"
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
                f"@GT_TRUE{self.label_counter}",
                "D;JGT",
                "@SP",
                "A=M-1",
                "M=0",  # false
                f"@GT_END{self.label_counter}",
                "0;JMP",
                f"(GT_TRUE{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"(GT_END{self.label_counter})"
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
                f"@LT_TRUE{self.label_counter}",
                "D;JLT",
                "@SP",
                "A=M-1",
                "M=0",  # false
                f"@LT_END{self.label_counter}",
                "0;JMP",
                f"(LT_TRUE{self.label_counter})",
                "@SP",
                "A=M-1",
                "M=-1", # true
                f"(LT_END{self.label_counter})"
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
        if command == 'C_PUSH':
            if segment == 'constant':
                asm = [
                    f"@{index}",
                    "D=A",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]
                self.file.write("\n".join(asm) + "\n")
            else:
                raise NotImplementedError(f"Push for segment {segment} not implemented.")
        elif command == 'C_POP':
            raise NotImplementedError(f"Pop command not implemented.")
        else:
            raise ValueError(f"Unknown command type: {command}")

    def close(self):
        self.file.close()