from enum import Enum, auto

class CommandType(Enum):
    C_ARITHMETIC = auto()  # add, sub, neg, eq, gt, lt, and, or, not
    C_PUSH = auto()        # push
    C_POP = auto()         # pop
    
    C_LABEL = auto()       # label
    C_GOTO = auto()        # goto
    C_IF = auto()          # if-goto
    C_FUNCTION = auto()    # function
    C_RETURN = auto()      # return
    C_CALL = auto()        # call