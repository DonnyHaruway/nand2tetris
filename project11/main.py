
#!/usr/bin/env python3
import sys
from pathlib import Path

from compiler.jack_analyzer import JackAnalyzer


def process_file(p: Path) -> None:
	if p.suffix.lower() != ".jack":
		return
	out = p.with_suffix('.vm')
	analyzer = JackAnalyzer(str(p), out)
	analyzer.analyze()
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
		print("Usage: python main.py {jack_file_or_directory}")
		sys.exit(1)
	process_target(sys.argv[1])


if __name__ == '__main__':
	main()
