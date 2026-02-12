from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    SYMBOL = auto()
    INT_CONST = auto()
    STRING_CONST = auto()
    IDENTIFIER = auto()

class Keyword(Enum):
    CLASS = "class"
    CONSTRUCTOR = "constructor"
    FUNCTION = "function"
    METHOD = "method"
    FIELD = "field"
    STATIC = "static"
    VAR = "var"
    INT = "int"
    CHAR = "char"
    BOOLEAN = "boolean"
    VOID = "void"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"

class Symbol(Enum):
    LEFT_CURLY = "{"
    RIGHT_CURLY = "}"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_SQUARE = "["
    RIGHT_SQUARE = "]"
    DOT = "."
    COMMA = ","
    SEMICOLON = ";"
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    AMPERSAND = "&"
    PIPE = "|"
    LESS_THAN = "<"
    GREATER_THAN = ">"
    EQUAL = "="
    TILDE = "~"

