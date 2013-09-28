import ply.lex as lex

# List of token names.
tokens = (
   'ARROW',
   'LPAREN',
   'RPAREN',
          
   'NUMBER',
   'STRING',
          
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'FLOOR_DIVIDE',
   'MODULO',
   'EXP',
          
   'BIT_AND',
   'BIT_OR',
   'BIT_XOR',
   'BIT_INVR',
   'LSHIFT',
   'RSHIFT',
          
   'LOG_NEG',
   'AND',
   'OR',
          
   'NEW',
   'DELETE',
          
   'LT',
   'LE',
   'EQ',
   'NE',
   'GE',
   'GT',
          
   'ASSIGNMENT',
          
   'SELECTOR',
   'SEPARATOR',
   'SEMICOLON',

   'EVENT_INTRO',

   'BOOL_LITERAL',

   'NAME'
)

def t_NUMBER(t):
    r'(\+|\-)?[0-9]+(\.[0-9]+((e|E)(\+|\-)?[0-9]+)?)?'
    t.value = eval(t.value)
    return t

t_NAME = r'[a-zA-Z][a-zA-Z0-9_]*'

t_ARROW   = r'->'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_FLOOR_DIVIDE = r'//'
t_MODULO = r'%'
t_EXP = r'\*\*'
t_LOG_NEG = r'!'

t_AND = r'&&'
t_OR = r'\|\|'

t_BIT_AND = r'&'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'
t_BIT_INVR = r'\~'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

t_LT = r'<'
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_GT = r'>'

t_ASSIGNMENT = r'='

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_SELECTOR = r'\.'
t_SEPARATOR = r','

t_SEMICOLON = r';'

t_EVENT_INTRO = r'\#'

def t_UNDEF(t):
    r'undefined'

def t_STRING(t):
    r'"[^\n"]*"'
    t.value = eval(t.value) # eval("'''%s'''" % t.value[1:-1])
    return t

def t_BOOL_LITERAL(t):
    r'True|False'
    t.value = eval(t.value)
    return t

def t_NEW(t):
    r'new'
    return t

def t_DELETE(t):
    r'delete'
    return t



t_ignore = ' \n\t'


# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def main():
    data = '''"abc\\nabcd" '''
    lexer.input(data)

    print "Source: %s" % data
    print "-----------------------------------------------"

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

if __name__ == '__main__':
    main()
