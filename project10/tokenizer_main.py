#!/usr/bin/env python3
import sys
from pathlib import Path

from compiler.jack_tokenizer import JackTokenizer
from compiler.token_types import TokenType


def write_tokens_xml(tokenizer: JackTokenizer, out_path: str) -> None:
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("<tokens>\n")
        for tok in tokenizer.tokens:
            t_type = tok['type']
            val = tok['value']
            if t_type == TokenType.KEYWORD:
                tag = 'keyword'
            elif t_type == TokenType.SYMBOL:
                tag = 'symbol'
                val = str(val).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            elif t_type == TokenType.INT_CONST:
                tag = 'integerConstant'
                val = str(val)
            elif t_type == TokenType.STRING_CONST:
                tag = 'stringConstant'
            elif t_type == TokenType.IDENTIFIER:
                tag = 'identifier'
            else:
                continue
            f.write(f"<{tag}> {val} </{tag}>\n")
        f.write("</tokens>\n")


def process_file(p: Path) -> None:
    if p.suffix.lower() != '.jack':
        return
    out = p.with_name(p.stem + 'T.xml')
    tokenizer = JackTokenizer(str(p))
    write_tokens_xml(tokenizer, str(out))
    print(f"Wrote: {out}")


def process_target(target: str) -> None:
    p = Path(target)
    if p.is_dir():
        for f in sorted(p.iterdir()):
            if f.suffix.lower() == '.jack':
                process_file(f)
    elif p.is_file():
        process_file(p)
    else:
        print(f"Target not found: {target}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python tokenizer_main.py {jack_file_or_directory}")
        sys.exit(1)
    process_target(sys.argv[1])


if __name__ == '__main__':
    main()
