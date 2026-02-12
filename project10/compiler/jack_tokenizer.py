import re
from token_types import TokenType, Keyword, Symbol

class JackTokenizer:
    def __init__(self, input_file : str):
        self.input_file = input_file
        self.tokens = []
        self.current_token_index = -1

        # Read file
        with open(self.input_file, 'r', encoding='utf-8') as f:
            src = f.read()

        # Tokenize
        symbols = {s.value for s in Symbol}
        keywords = {k.value for k in Keyword}

        i = 0
        n = len(src)
        while i < n:
            c = src[i]
            # Skip whitespace
            if c.isspace():
                i += 1
                continue

            # String constant
            if c == '"':
                i += 1
                start = i
                while i < n and src[i] != '"':
                    i += 1
                value = src[start:i]
                self.tokens.append({'type': TokenType.STRING_CONST, 'value': value})
                i += 1
                continue

            # Comments
            if c == '/':
                if i + 1 < n:
                    if src[i+1] == '/':  # 行コメント //
                        i = src.find('\n', i)
                        if i == -1: i = n # ファイル末尾まで
                        continue
                    elif src[i+1] == '*':  # ブロックコメント /*
                        end_index = src.find('*/', i + 2)
                        if end_index != -1:
                            i = end_index + 2
                            continue

            # Symbol
            if c in symbols:
                self.tokens.append({'type': TokenType.SYMBOL, 'value': c})
                i += 1
                continue

            # Integer constant
            if c.isdigit():
                start = i
                while i < n and src[i].isdigit():
                    i += 1
                value = int(src[start:i])
                self.tokens.append({'type': TokenType.INT_CONST, 'value': value})
                continue

            # Identifier or keyword
            if c.isalpha() or c == '_':
                start = i
                while i < n and (src[i].isalnum() or src[i] == '_'):
                    i += 1
                word = src[start:i]
                if word in keywords:
                    self.tokens.append({'type': TokenType.KEYWORD, 'value': word})
                else:
                    self.tokens.append({'type': TokenType.IDENTIFIER, 'value': word})
                continue

            # If we reach here, skip unknown character
            i += 1

    def has_more_tokens(self) -> bool:
        return self.current_token_index + 1 < len(self.tokens)
    
    def advance(self) -> None:
        if self.has_more_tokens():
            self.current_token_index += 1

    def token_type(self) -> TokenType:
        if not (0 <= self.current_token_index < len(self.tokens)):
            return None
        return self.tokens[self.current_token_index]['type']
    
    def keyword(self):
        if self.token_type() == TokenType.KEYWORD:
            return self.tokens[self.current_token_index]['value']
        return None
    
    def symbol(self):
        if self.token_type() == TokenType.SYMBOL:
            return self.tokens[self.current_token_index]['value']
        return None
    
    def identifier(self):
        if self.token_type() == TokenType.IDENTIFIER:
            return self.tokens[self.current_token_index]['value']
        return None
    
    def int_val(self):
        if self.token_type() == TokenType.INT_CONST:
            return self.tokens[self.current_token_index]['value']
        return None
    
    def string_val(self):
        if self.token_type() == TokenType.STRING_CONST:
            return self.tokens[self.current_token_index]['value']
        return None