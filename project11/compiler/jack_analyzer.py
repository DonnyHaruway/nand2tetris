from .compilation_engine import CompilationEngine
from .jack_tokenizer import JackTokenizer
from .vm_writer import VMWriter
from .symbol_table import SymbolTable
from pathlib import Path

class JackAnalyzer:
    def __init__(self, input_file: str, output_file: Path):
        self.tokenizer = JackTokenizer(input_file)
        self.output_path = output_file

    def analyze(self):
        symbol_table = SymbolTable()
        with self.output_path.open('w') as f:
            vm_writer = VMWriter(f)
            self.engine = CompilationEngine(self.tokenizer, symbol_table, vm_writer)
            self.engine.compile_class()