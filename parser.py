import ply.yacc as yacc
import ast

from lexer import tokens


def p_rules(p):
    ''' rules : rule_list '''
    p[0] = ""
    for r in p[1]:
        p[0] += "%s;" % r

def p_rule_list(p):
    ''' rule_list : rule SEMICOLON rule_list
                  | rule
                  | empty '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3];
    else:
        if p[1] != None:
            p[0] = [p[1]]
        else:
            p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_rule(p):
    ''' rule : LPAREN condition_list RPAREN ARROW LPAREN action_list RPAREN '''
    p[0] = "(%s)->(%s)" % (p[2], p[6])

def p_condition_list(p):
    ''' condition_list : condition SEPARATOR condition_list
                       | condition '''
    if len(p) > 2:
        p[0] = "%s, %s" % (p[1], p[3])
    else:
        p[0] = p[1]


# CONDITION

def p_condition(p):
    ''' condition : or_test
                  | event '''
    p[0] = p[1]

def p_event(p):
    ''' event : EVENT_INTRO NAME LPAREN RPAREN '''
    p[0] = p[1]

def p_or_test(p):
    ''' or_test : and_test OR or_test 
                | and_test'''
    if len(p) > 2:
        p[0] = "%s || %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_and_test(p):
    ''' and_test : not_test AND and_test 
                 | not_test '''
    if len(p) > 2:
        p[0] = "%s && %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_not_test(p):
    ''' not_test : LOG_NEG not_test
                 | comparison '''
    if len(p) == 3:
        p[0] = "!%s" % p[2]
    else:
        p[0] = p[1]

def p_comparison(p):
    ''' comparison : expr comp_op expr
                   | expr '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "%s %s %s" % (p[1], p[2], p[3])

def p_comp_op(p):
    ''' comp_op : LT 
                | LE 
                | EQ 
                | NE 
                | GE 
                | GT '''
    p[0] = p[1]

def p_expr(p):
    ''' expr : xor_expr BIT_OR expr 
             | xor_expr '''
    if len(p) > 2:
        p[0] = "%s | %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_xor_expr(p):
    ''' xor_expr : and_expr BIT_XOR xor_expr 
                 | and_expr '''
    if len(p) > 2:
        p[0] = "%s ^ %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_and_expr(p):
    ''' and_expr : shift_expr BIT_AND and_expr 
                 | shift_expr '''
    if len(p) > 2:
        p[0] = "%s & %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_shift_expr(p):
    ''' shift_expr : arithm_expr LSHIFT shift_expr 
                   | arithm_expr RSHIFT shift_expr
                   | arithm_expr '''
    if len(p) > 2:
        p[0] = "%s %s %s" % (p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_arithm_expr(p):
    ''' arithm_expr : selection '''
    p[0] = p[1]


# ACTION

def p_action_list(p):
    ''' action_list : action SEPARATOR action_list
                    | action '''
    if len(p) > 2:
        p[0] = "%s, %s" % ([1], p[3])
    else:
        p[0] = p[1]

def p_action_name(p):
    ''' action : selection '''
    p[0] = p[1]

def p_action_new(p):
    ''' action : NEW variable '''
    if len(p) == 3:
        p[0] = "new %s" % p[2]

def p_variable(p):
    ''' variable : NAME '''
    p[0] = p[1]

def p_selection(p):
    ''' selection : variable SELECTOR selection_path 
                  | variable '''

    if len(p) > 2:
        p[0] = p[1] + "." + p[3]
    else:
        p[0] = p[1]

def p_selection_path(p):
    ''' selection_path : NAME SELECTOR selection_path
                       | NAME '''
    
    if len(p) > 2:
        p[0] = p[1] + "." + p[3]
    else:
        p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Build the parser
parser = yacc.yacc()

def main():
    while True:
        try:
            s = raw_input('rule> ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print result

if __name__ == '__main__':
    main()
