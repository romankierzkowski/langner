from lefep import lexer
import sys

for line in sys.stdin.xreadlines():
	lexer.input(line)
	while True:
		tok = lexer.token()
		if not tok: break
		print tok

