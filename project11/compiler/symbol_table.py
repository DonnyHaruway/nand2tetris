class SymbolTable:
    def __init__(self):
        # クラススコープ (STATIC, FIELD)
        self.class_symbols = {}
        # サブルーチンスコープ (ARG, VAR)
        self.subroutine_symbols = {}
        # カウンタ
        self.counts = {
            'STATIC': 0,
            'FIELD': 0,
            'ARG': 0,
            'VAR': 0
        }

    def start_subroutine(self):
        self.subroutine_symbols = {}
        self.counts['ARG'] = 0
        self.counts['VAR'] = 0

    def define(self, name, type, kind):
        if kind in ['STATIC', 'FIELD']:
            self.class_symbols[name] = (type, kind, self.var_count(kind))
            self.counts[kind] += 1
        elif kind in ['ARG', 'VAR']:
            self.subroutine_symbols[name] = (type, kind, self.var_count(kind))
            self.counts[kind] += 1

    def var_count(self, kind):
        return self.counts[kind]

    def kind_of(self, name):
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name][1]
        elif name in self.class_symbols:
            return self.class_symbols[name][1]
        else:
            return None

    def type_of(self, name):
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name][0]
        elif name in self.class_symbols:
            return self.class_symbols[name][0]
        else:
            return None

    def index_of(self, name):
        if name in self.subroutine_symbols:
            return self.subroutine_symbols[name][2]
        elif name in self.class_symbols:
            return self.class_symbols[name][2]
        else:
            return None