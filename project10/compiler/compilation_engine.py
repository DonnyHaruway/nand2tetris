from .syntax_types import *
from .token_types import *
from .jack_tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, output) -> None:
        self.tokenizer = tokenizer
        self.output = output
        self.indent_level = 0
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self) -> None:
        self._write_start_tag(ProgramStructureType.CLASS.value)
        self._write_xml_token()  # 'class'
        self._write_xml_token()  # className (identifier)
        self._write_xml_token()  # '{'

        while self.tokenizer.keyword() in {Keyword.STATIC.value, Keyword.FIELD.value}:
            self.compile_class_var_dec()
        while self.tokenizer.keyword() in {Keyword.CONSTRUCTOR.value, Keyword.FUNCTION.value, Keyword.METHOD.value}:
            self.compile_subroutine()

        self._write_xml_token()  # '}'
        self._write_end_tag(ProgramStructureType.CLASS.value)

    
    def compile_class_var_dec(self) -> None:
        self._write_start_tag(ProgramStructureType.CLASS_VAR_DEC.value)
        self._write_xml_token()  # 'static' | 'field'
        self._write_xml_token()  # type
        self._write_xml_token()  # varName
        while self.tokenizer.symbol() == ',':
            self._write_xml_token()  # ','
            self._write_xml_token()  # varName
        self._write_xml_token()  # ';'
        self._write_end_tag(ProgramStructureType.CLASS_VAR_DEC.value)

    def compile_subroutine(self) -> None:
        self._write_start_tag(ProgramStructureType.SUBROUTINE_DEC.value)
        self._write_xml_token()  # 'constructor' | 'function' | 'method'
        self._write_xml_token()  # 'void' | type
        self._write_xml_token()  # subroutineName (identifier)
        self._write_xml_token()  # '('
        self.compile_parameter_list()
        self._write_xml_token()  # ')'
        # Subroutine body
        self._write_start_tag(ProgramStructureType.SUBROUTINE_BODY.value)
        self._write_xml_token()  # '{'
        while self.tokenizer.keyword() == Keyword.VAR.value:
            self.compile_var_dec()
        self.compile_statements()
        self._write_xml_token()  # '}'
        self._write_end_tag(ProgramStructureType.SUBROUTINE_BODY.value)
        self._write_end_tag(ProgramStructureType.SUBROUTINE_DEC.value)

    def compile_parameter_list(self) -> None:
        self._write_start_tag(ProgramStructureType.PARAMETER_LIST.value)
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            self._write_xml_token()  # type
            self._write_xml_token()  # varName
            while self.tokenizer.symbol() == ',':
                self._write_xml_token()  # ','
                self._write_xml_token()  # type
                self._write_xml_token()  # varName
        self._write_end_tag(ProgramStructureType.PARAMETER_LIST.value)

    def compile_var_dec(self) -> None:
        self._write_start_tag(ProgramStructureType.VAR_DEC.value)
        self._write_xml_token()  # 'var'
        self._write_xml_token()  # type
        self._write_xml_token()  # varName
        while self.tokenizer.symbol() == ',':
            self._write_xml_token()  # ','
            self._write_xml_token()  # varName
        self._write_xml_token()  # ';'
        self._write_end_tag(ProgramStructureType.VAR_DEC.value)

    def compile_statements(self) -> None:
        self._write_start_tag(StatementType.STATEMENTS.value)
        while self.tokenizer.keyword() in {
            Keyword.LET.value,
            Keyword.IF.value,
            Keyword.WHILE.value,
            Keyword.DO.value,
            Keyword.RETURN.value
        }:
            if self.tokenizer.keyword() == Keyword.LET.value:
                self.compile_let()
            elif self.tokenizer.keyword() == Keyword.IF.value:
                self.compile_if()
            elif self.tokenizer.keyword() == Keyword.WHILE.value:
                self.compile_while()
            elif self.tokenizer.keyword() == Keyword.DO.value:
                self.compile_do()
            elif self.tokenizer.keyword() == Keyword.RETURN.value:
                self.compile_return()
        self._write_end_tag(StatementType.STATEMENTS.value)

    def compile_do(self) -> None:
        self._write_start_tag(StatementType.DO_STATEMENT.value)
        self._write_xml_token()  # 'do'
        self.compile_subroutine_call()
        self._write_xml_token()  # ';'
        self._write_end_tag(StatementType.DO_STATEMENT.value)

    def compile_let(self) -> None:
        self._write_start_tag(StatementType.LET_STATEMENT.value)
        self._write_xml_token()  # 'let'
        self._write_xml_token()  # varName
        if self.tokenizer.symbol() == '[':
            self._write_xml_token()  # '['
            self.compile_expression()
            self._write_xml_token()  # ']'
        self._write_xml_token()  # '='
        self.compile_expression()
        self._write_xml_token()  # ';'
        self._write_end_tag(StatementType.LET_STATEMENT.value)

    def compile_while(self) -> None:
        self._write_start_tag(StatementType.WHILE_STATEMENT.value)
        self._write_xml_token()  # 'while'
        self._write_xml_token()  # '('
        self.compile_expression()
        self._write_xml_token()  # ')'
        self._write_xml_token()  # '{'
        self.compile_statements()
        self._write_xml_token()  # '}'
        self._write_end_tag(StatementType.WHILE_STATEMENT.value)

    def compile_return(self) -> None:
        self._write_start_tag(StatementType.RETURN_STATEMENT.value)
        self._write_xml_token()  # 'return'
        if self.tokenizer.symbol() != ';':
            self.compile_expression()
        self._write_xml_token()  # ';'
        self._write_end_tag(StatementType.RETURN_STATEMENT.value)

    def compile_if(self) -> None:
        self._write_start_tag(StatementType.IF_STATEMENT.value)
        self._write_xml_token()  # 'if'
        self._write_xml_token()  # '('
        self.compile_expression()
        self._write_xml_token()  # ')'
        self._write_xml_token()  # '{'
        self.compile_statements()
        self._write_xml_token()  # '}'
        if self.tokenizer.keyword() == Keyword.ELSE.value:
            self._write_xml_token()  # 'else'
            self._write_xml_token()  # '{'
            self.compile_statements()
            self._write_xml_token()  # '}'
        self._write_end_tag(StatementType.IF_STATEMENT.value)

    def compile_expression(self) -> None:
        self._write_start_tag(ExpressionType.EXPRESSION.value)
        self.compile_term()
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in {
            Symbol.PLUS.value,
            Symbol.MINUS.value,
            Symbol.ASTERISK.value,
            Symbol.SLASH.value,
            Symbol.AMPERSAND.value,
            Symbol.PIPE.value,
            Symbol.LESS_THAN.value,
            Symbol.GREATER_THAN.value,
            Symbol.EQUAL.value
        }:
            self._write_xml_token()  # op
            self.compile_term()
        self._write_end_tag(ExpressionType.EXPRESSION.value)

    def compile_term(self) -> None:
        self._write_start_tag(ExpressionType.TERM.value)
        t_type = self.tokenizer.token_type()
        if t_type in {TokenType.INT_CONST, TokenType.STRING_CONST}:
            self._write_xml_token()  # integerConstant | stringConstant
        elif t_type == TokenType.KEYWORD and self.tokenizer.keyword() in {
            Keyword.TRUE.value,
            Keyword.FALSE.value,
            Keyword.NULL.value,
            Keyword.THIS.value
        }:
            self._write_xml_token()  # keywordConstant
        elif t_type == TokenType.IDENTIFIER:
            next_token = self.tokenizer.peek_next_token()
            if next_token and next_token['value'] == "[":
                self._write_xml_token()  # varName
                self._write_xml_token()  # '['
                self.compile_expression()
                self._write_xml_token()  # ']'
            elif next_token['value'] in {'(', '.'}:
                self.compile_subroutine_call()
            else:
                self._write_xml_token()  # varName

        elif t_type == TokenType.SYMBOL and self.tokenizer.symbol() in {'(', '-','~'}:
            if self.tokenizer.symbol() == '(':
                self._write_xml_token()  # '('
                self.compile_expression()
                self._write_xml_token()  # ')'
            else:
                self._write_xml_token()  # unaryOp
                self.compile_term()
        else:
            raise ValueError("Unexpected token in term")
        self._write_end_tag(ExpressionType.TERM.value)

    def compile_expression_list(self) -> None:
        self._write_start_tag(ExpressionType.EXPRESSION_LIST.value)
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            self.compile_expression()
            while self.tokenizer.symbol() == ',':
                self._write_xml_token()  # ','
                self.compile_expression()
        self._write_end_tag(ExpressionType.EXPRESSION_LIST.value)

    def compile_subroutine_call(self) -> None:
        # self._write_start_tag(ExpressionType.SUBROUTINE_CALL.value)
        self._write_xml_token()  # subroutineName | className | varName
        if self.tokenizer.symbol() == '.':
            self._write_xml_token()  # '.'
            self._write_xml_token()  # subroutineName
        self._write_xml_token()  # '('
        self.compile_expression_list()
        self._write_xml_token()  # ')'
        # self._write_end_tag(ExpressionType.SUBROUTINE_CALL.value)

    def _write_xml_token(self) -> None:
        """現在のトークンを XML 形式で出力して 1 つ進める"""
        t_type = self.tokenizer.token_type()

        tag = ""
        val = ""
        
        if t_type == TokenType.KEYWORD:
            tag = "keyword"
            val = self.tokenizer.keyword()
        elif t_type == TokenType.SYMBOL:
            tag = "symbol"
            val = self.tokenizer.symbol()
            # XMLで特別な意味を持つ記号のエスケープ処理
            val = val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        elif t_type == TokenType.INT_CONST:
            tag = "integerConstant"
            val = str(self.tokenizer.int_val())
        elif t_type == TokenType.STRING_CONST:
            tag = "stringConstant"
            val = self.tokenizer.string_val()
        elif t_type == TokenType.IDENTIFIER:
            tag = "identifier"
            val = self.tokenizer.identifier()

        self.output.write('  ' * self.indent_level)
        self.output.write(f"<{tag}> {val} </{tag}>\n")
        self.tokenizer.advance()

    def _write_start_tag(self, tag: str) -> None:
        self.output.write('  ' * self.indent_level)
        self.output.write(f"<{tag}>\n")
        self.indent_level += 1

    def _write_end_tag(self, tag: str) -> None:
        self.indent_level -= 1
        self.output.write('  ' * self.indent_level)
        self.output.write(f"</{tag}>\n")