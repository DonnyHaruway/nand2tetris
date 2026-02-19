class VMWriter:

    SEGMENT_MAP = {
        'CONST': 'constant',
        'ARG': 'argument',
        'VAR': 'local',
        'STATIC': 'static',
        'FIELD': 'this',
        'THAT': 'that',
        'POINTER': 'pointer',
        'TEMP': 'temp'
    }

    def __init__(self, output_file):
        self.output_file = output_file
        self.INDENT = '    '

    def write_push(self, segment, index):
        self.output_file.write(f'{self.INDENT}push {self.SEGMENT_MAP[segment]} {index}\n')

    def write_pop(self, segment, index):
        self.output_file.write(f'{self.INDENT}pop {self.SEGMENT_MAP[segment]} {index}\n')

    def write_arithmetic(self, command):
        if command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            self.output_file.write(f'{self.INDENT}{command}\n')
        else:
            raise ValueError(f'Invalid arithmetic command: {command}')

    def write_label(self, label):
        self.output_file.write(f'label {label}\n')

    def write_goto(self, label):
        self.output_file.write(f'{self.INDENT}goto {label}\n')

    def write_if(self, label):
        self.output_file.write(f'{self.INDENT}if-goto {label}\n')

    def write_call(self, name, n_args):
        self.output_file.write(f'{self.INDENT}call {name} {n_args}\n')

    def write_function(self, name, n_locals):
        self.output_file.write(f'function {name} {n_locals}\n')

    def write_return(self):
        self.output_file.write(f'{self.INDENT}return\n')

    def close(self):
        self.output_file.close()