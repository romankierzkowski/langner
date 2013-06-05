import ply.yacc as yacc
import ast
import re

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
    ''' event : EVENT_INTRO NAME LPAREN var_declar RPAREN '''
    p[0] = "#%s(%s)" % (p[2], p[4])

def p_var_declar(p):
    ''' var_declar : var_list
                   | empty
    '''
    p[0] = ""
    if p[1] != None: 
        for r in p[1][:-1]:
            p[0] += "%s, " % r
        p[0] += p[1][-1]

def p_var_list(p):
    ''' var_list : variable SEPARATOR var_list
                 | variable
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

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
    ''' arithm_expr : term PLUS arithm_expr 
                    | term MINUS arithm_expr
                    | term '''
    if len(p) > 2:
        p[0] = "%s %s %s" % (p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    ''' term : factor TIMES term 
             | factor DIVIDE term
             | factor MODULO term
             | factor FLOOR_DIVIDE term
             | factor '''
    if len(p) > 2:
        p[0] = "%s %s %s" % (p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    ''' factor : PLUS factor
               | MINUS factor
               | BIT_INVR factor
               | power '''
    if len(p) == 3:
        p[0] = "%s%s" % (p[1], p[2])
    else:
        p[0] = p[1]


def p_power(p):
    ''' power : atom EXP factor 
              | atom '''
    if len(p) > 2:
        p[0] = "%s ** %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_string_atom(p):
    ''' atom : STRING '''
    value = list(repr(p[1]))
    value[0] = value[-1] = '"'
    p[0] = "".join(value)

def p_atom(p):
    ''' atom : NUMBER
             | TRUE
             | FALSE
             | LPAREN or_test RPAREN
             | selection
             | function_exec '''
    if len(p) == 4:
        p[0] = "(%s)" % p[2]
    else:
        p[0] = p[1]

def p_function_exec(p):
    ''' function_exec : NAME LPAREN params RPAREN
    '''
    p[0] = "%s(%s)" % (p[1], p[3])

def p_params(p):
    ''' params : test_list
               | empty
    '''
    p[0] = ""
    if p[1] != None: 
        for r in p[1][:-1]:
            p[0] += "%s, " % r
        p[0] += p[1][-1]

def p_test_list(p):
    ''' test_list : or_test SEPARATOR test_list
                  | or_test 
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# ACTION

def p_action_list(p):
    ''' action_list : action SEPARATOR action_list
                    | action '''
    if len(p) > 2:
        p[0] = "%s, %s" % (p[1], p[3])
    else:
        p[0] = p[1]

def p_action_assignment(p):
    ''' action : strict_selection ASSIGNMENT or_test '''
    p[0] = "%s = %s" % (p[1], p[3])

def p_action_function(p):
    ''' action : function_exec '''
    p[0] = p[1]

def p_action_new(p):
    ''' action : NEW variable '''
    if len(p) == 3:
        p[0] = "new %s" % p[2]

def p_action_delete(p):
    ''' action : DELETE variable '''
    if len(p) == 3:
        p[0] = "delete %s" % p[2]

def p_variable(p):
    ''' variable : NAME '''
    p[0] = p[1]

def p_selection(p):
    ''' selection : strict_selection 
                  | variable '''
    p[0] = p[1]

def p_strict_selection(p):
    ''' strict_selection : variable SELECTOR selection_path '''
    p[0] = p[1] + "." + p[3]

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
