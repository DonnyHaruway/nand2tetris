// メインループ: キー入力をチェックし、
// 押されていなければ(D=0)WHITEへ、
// 押されていれば(D!=0)BLACKへ飛ぶ
(END)
    @KBD
    D=M
    @WHITE
    D;JEQ
    @BLACK
    0;JMP

// 画面を白 (0) で埋める
(WHITE)
    @i
    M=0         // i = 0
(LOOP_WHITE)
    // 1. アドレスを計算 (D = SCREEN + i)
    @SCREEN
    D=A
    @i
    D=D+M
    // 2. 計算したアドレスをptr変数に保存
    @ptr
    M=D
    // 3. Aレジスタにアドレスをセット (A = ptr = SCREEN + i)
    A=M
    // 4. そのアドレスのメモリを 0 (白) にする
    M=0

    // 5. ループカウンタを進める
    @i
    M=M+1
    D=M         // D = i
    @8192       // 8192回ループしたか？
    D=D-A       // D = i - 8192
    @END
    D;JEQ       // もし i == 8192 なら (全画面埋めたら) END に戻る
    @LOOP_WHITE
    0;JMP       // まだなら LOOP_WHITE を続ける

// 画面を黒 (-1) で埋める
(BLACK)
    @i
    M=0         // i = 0
(LOOP_BLACK)
    // 1. アドレスを計算 (D = SCREEN + i)
    @SCREEN
    D=A
    @i
    D=D+M
    // 2. 計算したアドレスをptr変数に保存
    @ptr
    M=D
    // 3. Aレジスタにアドレスをセット (A = ptr = SCREEN + i)
    A=M
    // 4. そのアドレスのメモリを -1 (黒) にする
    M=-1

    // 5. ループカウンタを進める
    @i
    M=M+1
    D=M         // D = i
    @8192       // 8192回ループしたか？
    D=D-A       // D = i - 8192
    @END
    D;JEQ       // もし i == 8192 なら (全画面埋めたら) END に戻る
    @LOOP_BLACK
    0;JMP       // まだなら LOOP_BLACK を続ける

// 使用する変数 (ptr) のためのメモリ確保
@ptr