from .syntax_types import *
from .token_types import *
from .jack_tokenizer import JackTokenizer
from .vm_writer import VMWriter
from .symbol_table import SymbolTable

class CompilationEngine:

    ARITHMETIC_MAP = {
        '+': 'add', '-': 'sub', '&': 'and', '|': 'or',
        '<': 'lt', '>': 'gt', '=': 'eq'
    }

    def __init__(self, tokenizer: JackTokenizer, symbol_table: SymbolTable, vm_writer: VMWriter) -> None:
        self.tokenizer = tokenizer
        self.symbol_table = symbol_table
        self.vm_writer = vm_writer
        self.class_name = ""
        self.label_index = 0
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self) -> None:
        self._eat()  # 'class'
        self.class_name = self._eat()  # className
        self._eat()  # '{'

        while self.tokenizer.keyword() in {Keyword.STATIC.value, Keyword.FIELD.value}:
            self.compile_class_var_dec()
        while self.tokenizer.keyword() in {Keyword.CONSTRUCTOR.value, Keyword.FUNCTION.value, Keyword.METHOD.value}:
            self.compile_subroutine()

        self._eat()  # '}'
    
    def compile_class_var_dec(self) -> None:
        kind = self._eat().upper()  # 'static' | 'field'
        var_type = self._eat()  # type
        var_name = self._eat()  # varName
        self.symbol_table.define(var_name, var_type, kind) # シンボルテーブルに定義
        while self.tokenizer.symbol() == ',':
            self._eat()  # ','
            var_name = self._eat()  # varName
            self.symbol_table.define(var_name, var_type, kind) # シンボルテーブルに定義
        self._eat()  # ';'

    def compile_subroutine(self) -> None:
        self.symbol_table.start_subroutine()  # サブルーチンごとにシンボルテーブルをリセット
        subroutine_kind = self._eat()  # 'constructor' | 'function' | 'method'
        if subroutine_kind == 'method':
            self.symbol_table.define("this", self.class_name, "ARG") # メソッドの場合、thisをARGに定義
        self._eat()  # 'void' | type
        subroutine_name = self._eat()  # subroutineName
        self._eat()  # '('
        self.compile_parameter_list()
        self._eat()  # ')'

        self._eat()  # '{'
        while self.tokenizer.keyword() == Keyword.VAR.value:
            self.compile_var_dec()
        self.vm_writer.write_function(f"{self.class_name}.{subroutine_name}", self.symbol_table.var_count("VAR")) # VMWriterに関数定義を書き込む
        if subroutine_kind == 'constructor':
            # フィールドの数だけメモリを確保してthisをセット
            n_fields = self.symbol_table.var_count("FIELD")
            self.vm_writer.write_push("CONST", n_fields)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)  # thisを0番ポインタにセット
        elif subroutine_kind == 'method':
            # メソッドの場合、呼び出し元から渡されたthisをARG 0にセットしてからthisを0番ポインタにセット
            self.vm_writer.write_push("ARG", 0)  # thisをARG 0にセット
            self.vm_writer.write_pop("POINTER", 0)  # thisを0番ポインタにセット
        self.compile_statements()
        self._eat()  # '}'

    def compile_parameter_list(self) -> None:
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            p_type = self._eat()  # type
            p_name = self._eat()  # varName
            self.symbol_table.define(p_name, p_type, "ARG") # シンボルテーブルに定義
            while self.tokenizer.symbol() == ',':
                self._eat()  # ','
                p_type = self._eat()  # type
                p_name = self._eat()  # varName
                self.symbol_table.define(p_name, p_type, "ARG") # シンボルテーブルに定義

    def compile_var_dec(self) -> None:
        kind = self._eat().upper()  # 'var'
        var_type = self._eat()  # type
        var_name = self._eat()  # varName

        self.symbol_table.define(var_name, var_type, kind) # シンボルテーブルに定義
        while self.tokenizer.symbol() == ',':
            self._eat()  # ','
            var_name = self._eat()  # varName
            self.symbol_table.define(var_name, var_type, kind) # シンボルテーブルに定義
        
        self._eat()  # ';'

    def compile_statements(self) -> None:
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

    def compile_do(self) -> None:
        self._eat()  # 'do'
        self.compile_subroutine_call()
        self._eat()  # ';'
        # 戻り値を捨てる（重要！）
        self.vm_writer.write_pop("TEMP", 0)

    def compile_let(self) -> None:
        self._eat()  # 'let'
        var_name = self._eat()
        
        is_array = (self.tokenizer.symbol() == '[')
        if is_array:
            # 1. アドレス計算 (a + i)
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.vm_writer.write_push(kind, idx)
            self._eat()  # '['
            self.compile_expression()
            self._eat()  # ']'
            self.vm_writer.write_arithmetic('add')
            # まだ pop pointer 1 はしない（右辺の計算で THAT が変わる可能性があるため）
            
        self._eat()  # '='
        self.compile_expression()  # 右辺の値を評価（スタックに積まれる）
        self._eat()  # ';'

        if is_array:
            # 2. トリッキーな代入処理
            self.vm_writer.write_pop('TEMP', 0)     # 右辺の値を一時避難
            self.vm_writer.write_pop('POINTER', 1)  # 保存しておいたアドレスを THAT へ
            self.vm_writer.write_push('TEMP', 0)    # 値を戻す
            self.vm_writer.write_pop('THAT', 0)     # 代入！
        else:
            # 通常の代入
            kind = self.symbol_table.kind_of(var_name)
            idx = self.symbol_table.index_of(var_name)
            self.vm_writer.write_pop(kind, idx)

    def compile_while(self) -> None:
        l1 = self._get_new_label()
        l2 = self._get_new_label()

        self._eat()  # 'while'
        self.vm_writer.write_label(l1)
        
        self._eat()  # '('
        self.compile_expression()
        self._eat()  # ')'

        self.vm_writer.write_arithmetic("not")
        self.vm_writer.write_if(l2)  # 条件が偽なら終了ラベルへ

        self._eat()  # '{'
        self.compile_statements()
        self._eat()  # '}'

        self.vm_writer.write_goto(l1)  # 条件判定へ戻る
        self.vm_writer.write_label(l2)

    def compile_return(self) -> None:
        self._eat()  # 'return'
        if self.tokenizer.symbol() != ';':
            self.compile_expression()
        else:
            # voidサブルーチンの場合は 0 をプッシュ
            self.vm_writer.write_push("CONST", 0)
        self.vm_writer.write_return()
        self._eat()  # ';'

    def compile_if(self) -> None:
        l_true = self._get_new_label()
        l_false = self._get_new_label()
        l_end = self._get_new_label()

        self._eat()  # 'if'
        self._eat()  # '('
        self.compile_expression()  # 条件式の評価（スタックに結果が積まれる）
        self._eat()  # ')'

        # 条件が真なら l_true へ、そうでなければ l_false へ
        self.vm_writer.write_if(l_true)
        self.vm_writer.write_goto(l_false)

        # --- IFブロック ---
        self.vm_writer.write_label(l_true)
        self._eat()  # '{'
        self.compile_statements()
        self._eat()  # '}'

        if self.tokenizer.keyword() == Keyword.ELSE.value:
            # elseがある場合は、ifブロック終了後に全体を抜ける
            self.vm_writer.write_goto(l_end)
            self.vm_writer.write_label(l_false)
            
            self._eat()  # 'else'
            self._eat()  # '{'
            self.compile_statements()
            self._eat()  # '}'
            
            self.vm_writer.write_label(l_end)
        else:
            # elseがない場合は、偽の時の飛び先をここにする
            self.vm_writer.write_label(l_false)

    def compile_expression(self) -> None:
        # 1. まず最初の項をコンパイル（スタックに値が1つ積まれる）
        self.compile_term()

        # 2. (演算子 項) の組み合わせが続く限り繰り返す
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in {
            '+', '-', '*', '/', '&', '|', '<', '>', '='
        }:
            op = self._eat() # 演算子をキープ
            
            # 3. 次の項をコンパイル（スタックに2つ目の値が積まれる）
            self.compile_term()
            
            # 4. 最後に演算命令を出す（スタックの上の2つを使って計算）
            if op in self.ARITHMETIC_MAP:
                self.vm_writer.write_arithmetic(self.ARITHMETIC_MAP[op])
            elif op == '*':
                self.vm_writer.write_call("Math.multiply", 2)
            elif op == '/':
                self.vm_writer.write_call("Math.divide", 2)

    def compile_term(self) -> None:
        t_type = self.tokenizer.token_type()
        
        if t_type == TokenType.INT_CONST:
            self.vm_writer.write_push("CONST", self._eat())
            
        elif t_type == TokenType.KEYWORD:
            kw = self._eat()
            if kw == 'true':
                self.vm_writer.write_push("CONST", 0)
                self.vm_writer.write_arithmetic("not")
            elif kw in {'false', 'null'}:
                self.vm_writer.write_push("CONST", 0)
            elif kw == 'this':
                self.vm_writer.write_push("POINTER", 0)

        elif t_type == TokenType.IDENTIFIER:
            name = self._eat()  # まず名前を取得
            
            next_symbol = self.tokenizer.symbol() if self.tokenizer.token_type() == TokenType.SYMBOL else None

            if next_symbol == '[':
                # 1. ベースアドレス + インデックスの計算
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(kind, index)  # 配列のベースアドレスを積む
                
                self._eat()  # '['
                self.compile_expression()  # インデックス i を評価して積む
                self._eat()  # ']'
                
                self.vm_writer.write_arithmetic('add')  # スタック：[a+i] (アドレス)
                
                # 2. ポインタを設定して値を読み取る
                self.vm_writer.write_pop('POINTER', 1)  # THAT = a+i
                self.vm_writer.write_push('THAT', 0)    # *(a+i) をスタックに積む
                
            elif next_symbol in ['(', '.']:
                self.compile_subroutine_call(name)
                
            else:
                # ただの変数
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(kind, index)

        elif t_type == TokenType.STRING_CONST:
            string_val = self._eat()
            # 1. 文字列の長さ分のメモリを確保
            self.vm_writer.write_push("CONST", len(string_val))
            self.vm_writer.write_call("String.new", 1)
            
            # 2. 1文字ずつ appendChar を呼ぶ
            for char in string_val:
                self.vm_writer.write_push("CONST", ord(char)) # ASCIIコードをpush
                self.vm_writer.write_call("String.appendChar", 2)

        elif t_type == TokenType.SYMBOL and self.tokenizer.symbol() in {'-', '~'}:
            op = self._eat()
            self.compile_term() # 先に中身をスタックに積む
            if op == '-':
                self.vm_writer.write_arithmetic('neg')
            else:
                self.vm_writer.write_arithmetic('not')

        elif t_type == TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            self._eat()  # '('
            self.compile_expression() # 内部の式を評価（結果がスタックに積まれる）
            self._eat()  # ')'

    def compile_expression_list(self) -> int:
        count = 0
        if self.tokenizer.token_type() != TokenType.SYMBOL or self.tokenizer.symbol() != ')':
            self.compile_expression()
            count = 1
            while self.tokenizer.symbol() == ',':
                self._eat()  # ','
                self.compile_expression()
                count += 1
        return count

    def compile_subroutine_call(self, first_name: str = None) -> None:
        # 引数がない場合は、今のトークンを名前として使う（do文からの呼び出し用）
        name = first_name if first_name else self._eat()
        n_args = 0

        if self.tokenizer.symbol() == '.':
            # --- className.func() か objName.method() のケース ---
            self._eat()  # '.'
            subroutine_name = self._eat()
            
            # シンボルテーブルにあるか確認
            type_of_obj = self.symbol_table.type_of(name)
            if type_of_obj:
                # 【メソッド呼び出し】オブジェクトを第0引数としてpush
                kind = self.symbol_table.kind_of(name)
                index = self.symbol_table.index_of(name)
                self.vm_writer.write_push(kind, index)
                # 呼び出し名は "型.メソッド名" になる
                full_name = f"{type_of_obj}.{subroutine_name}"
                n_args = 1
            else:
                # 【関数/静的呼び出し】単なる "クラス名.関数名"
                full_name = f"{name}.{subroutine_name}"
        else:
            # --- 同一クラス内のメソッド呼び出し func() ---
            # 自分自身 (this) を第0引数としてpush
            self.vm_writer.write_push("POINTER", 0)
            full_name = f"{self.class_name}.{name}"
            n_args = 1

        self._eat()  # '('
        n_args += self.compile_expression_list()
        self._eat()  # ')'
        self.vm_writer.write_call(full_name, n_args)

    def _eat(self):
        token_value = ""
        t_type = self.tokenizer.token_type()

        if t_type == TokenType.KEYWORD:
            token_value = self.tokenizer.keyword()
        elif t_type == TokenType.SYMBOL:
            token_value = self.tokenizer.symbol()
        elif t_type == TokenType.IDENTIFIER:
            token_value = self.tokenizer.identifier()
        elif t_type == TokenType.INT_CONST:
            token_value = self.tokenizer.int_val()
        elif t_type == TokenType.STRING_CONST:
            token_value = self.tokenizer.string_val()
        else:
            raise ValueError("Unknown token type")
        
        self.tokenizer.advance()
        return token_value
    
    def _get_new_label(self):
        label = f"L{self.label_index}"
        self.label_index += 1
        return label