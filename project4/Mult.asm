@R3
M=1
@R2
M=0
(LOOP)
    // LOOP処理の開始
    @R3 
    D=M
    @R1
    D=D-M
    @END
    D;JGT
    // LOOP処理のうしろ
    @R0
    D=M
    @R2
    M=D+M
    @R3
    M=M+1
    @LOOP
    0;JMP
// 最後は無限ループ
(END)
    @END
    0;JMP