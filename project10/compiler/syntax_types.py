from enum import Enum


class ProgramStructureType(Enum):
    CLASS = "class"
    CLASS_VAR_DEC = "classVarDec"
    TYPE = "type"
    SUBROUTINE_DEC = "subroutineDec"
    PARAMETER_LIST = "parameterList"
    SUBROUTINE_BODY = "subroutineBody"
    VAR_DEC = "varDec"
    CLASS_NAME = "className"
    SUBROUTINE_NAME = "subroutineName"
    VAR_NAME = "varName"

class StatementType(Enum):
    STATEMENTS = "statements"
    STATEMENT = "statement"
    LET_STATEMENT = "letStatement"
    IF_STATEMENT = "ifStatement"
    WHILE_STATEMENT = "whileStatement"
    DO_STATEMENT = "doStatement"
    RETURN_STATEMENT = "returnStatement"

class ExpressionType(Enum):
    EXPRESSION = "expression"
    TERM = "term"
    SUBROUTINE_CALL = "subroutineCall"
    EXPRESSION_LIST = "expressionList"
    OP = "op"
    UNARY_OP = "unaryOp"
    KEYWORD_CONSTANT = "keywordConstant"