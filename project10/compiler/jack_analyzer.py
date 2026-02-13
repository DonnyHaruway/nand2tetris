from .compilation_engine import CompilationEngine
from .jack_tokenizer import JackTokenizer

class JackAnalyzer:
    def __init__(self, input_file: str, output_file: str):
        self.tokenizer = JackTokenizer(input_file)
        self.output_path = output_file

    def analyze(self):
        with open(self.output_path, 'w', encoding='utf-8') as f:
            self.engine = CompilationEngine(self.tokenizer, f)
            self.engine.compile_class()