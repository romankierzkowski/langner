import ply.yacc as yacc
from ast import *
import re

from lexer import tokens


def p_strategy(p):
    ''' strategy : rule_list '''
    p[0] = Strategy(p[1])

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
    p[0] = Rule(p[2], p[6])

def p_condition_list(p):
    ''' condition_list : condition SEPARATOR condition_list
                       | condition '''
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


# CONDITION

def p_condition(p):
    ''' condition : or_test
                  | event '''
    p[0] = p[1]

def p_event(p):
    ''' event : EVENT_INTRO NAME LPAREN var_declar RPAREN '''
    p[0] = Event(p[2], p[4])

def p_var_declar(p):
    ''' var_declar : var_list
                   | empty
    '''
    p[0] = p[1]

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
        p[0] = Or(p[1], p[3])
    else:
        p[0] = p[1]

def p_and_test(p):
    ''' and_test : not_test AND and_test 
                 | not_test '''
    if len(p) > 2:
        p[0] = And(p[1], p[3])
    else:
        p[0] = p[1]

def p_not_test(p):
    ''' not_test : LOG_NEG not_test
                 | comparison '''
    if len(p) == 3:
        p[0] = Not(p[2])
    else:
        p[0] = p[1]

def p_comparison_lt(p):
    ''' comparison : expr LT expr '''
    p[0] = LT(p[1], p[3])

def p_comparison_le(p):
    ''' comparison : expr LE expr '''
    p[0] = LE(p[1], p[3])

def p_comparison_eq(p):
    ''' comparison : expr EQ expr '''
    p[0] = EQ(p[1], p[3])

def p_comparison_ne(p):
    ''' comparison : expr NE expr '''
    p[0] = NE(p[1], p[3])

def p_comparison_ge(p):
    ''' comparison : expr GE expr '''
    p[0] = GE(p[1], p[3])

def p_comparison_gt(p):
    ''' comparison : expr GT expr '''
    p[0] = GT(p[1], p[3])

def p_comparison(p):
    ''' comparison : expr '''
    p[0] = p[1]

def p_expr(p):
    ''' expr : xor_expr BIT_OR expr 
             | xor_expr '''
    if len(p) > 2:
        p[0] = BitOr(p[1], p[3])
    else:
        p[0] = p[1]

def p_xor_expr(p):
    ''' xor_expr : and_expr BIT_XOR xor_expr 
                 | and_expr '''
    if len(p) > 2:
        p[0] = BitXor(p[1], p[3])
    else:
        p[0] = p[1]

def p_and_expr(p):
    ''' and_expr : shift_expr BIT_AND and_expr 
                 | shift_expr '''
    if len(p) > 2:
        p[0] = BitAnd(p[1], p[3])
    else:
        p[0] = p[1]

def p_shift(p):
    ''' shift_expr : arithm_expr '''
    p[0] = p[1]

def p_lshift(p):
    ''' shift_expr : arithm_expr LSHIFT shift_expr '''
    p[0] = LeftShift(p[1], p[3])

def p_rshift(p):
    ''' shift_expr : arithm_expr RSHIFT shift_expr '''
    p[0] = RightShift(p[1], p[3])

def p_arithm_expr(p):
    ''' arithm_expr : term '''
    p[0] = p[1]

def p_arithm_plus(p):
    ''' arithm_expr : term PLUS arithm_expr '''
    p[0] = Add(p[1], p[3])

def p_arithm_minus(p):
    ''' arithm_expr : term MINUS arithm_expr '''
    p[0] = Substract(p[1], p[3])

def p_term(p):
    ''' term : factor '''
    p[0] = p[1]

def p_term_times(p):
    ''' term : factor TIMES term '''
    p[0] = Multiply(p[1], p[3])

def p_term_divide(p):
    ''' term : factor DIVIDE term '''
    p[0] = Divide(p[1], p[3])

def p_term_modulo(p):
    ''' term : factor MODULO term '''
    p[0] = Modulo(p[1], p[3])

def p_term_floor_divide(p):
    ''' term : factor FLOOR_DIVIDE term '''
    p[0] = FloorDivide(p[1], p[3])

def p_factor(p):
    ''' factor : power '''
    p[0] = p[1]

def p_factor_plus(p):
    ''' factor : PLUS factor '''
    p[0] = p[2]

def p_factor_minus(p):
    ''' factor : MINUS factor '''
    p[0] = Negation(p[2])

def p_factor_inversion(p):
    ''' factor : BIT_INVR factor '''
    p[0] = Inversion(p[2])

def p_power(p):
    ''' power : atom EXP factor 
              | atom '''
    if len(p) > 2:
        p[0] = Power(p[1], p[3])
    else:
        p[0] = p[1]

def p_atom_string(p):
    ''' atom : STRING '''
    p[0] = StringLiteral(p[1])

def p_atom_number(p):
    ''' atom : NUMBER '''
    p[0] = NumberLiteral(p[1])

def p_atom_bool(p):
    ''' atom : BOOL_LITERAL '''
    p[0] = BooleanLiteral(p[1])

def p_atom_paren(p):
    ''' atom : LPAREN or_test RPAREN '''
    p[0] = p[2]

def p_atom(p):
    ''' atom : selection
             | function_exec '''
    p[0] = p[1]

def p_function_exec(p):
    ''' function_exec : NAME LPAREN params RPAREN '''
    p[0] = FunctionExecution(p[1], p[3])

def p_params(p):
    ''' params : test_list
               | empty
    '''
    p[0] = p[1]

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
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_action_assignment(p):
    ''' action : strict_selection ASSIGNMENT or_test '''
    p[0] = Assignment(p[1], p[3])

def p_action_function(p):
    ''' action : function_exec '''
    p[0] = p[1]

def p_action_new(p):
    ''' action : NEW variable '''
    p[0] = New(p[2])

def p_action_delete(p):
    ''' action : DELETE variable '''
    p[0] = Delete(p[2])

def p_variable(p):
    ''' variable : NAME '''
    p[0] = Variable(p[1])

def p_selection_strict(p):
    ''' selection : strict_selection '''
    p[0] = p[1]

def p_selection_variable(p):
    ''' selection : variable '''
    p[0] = Selection(p[1], None)

def p_strict_selection(p):
    ''' strict_selection : variable SELECTOR selection_path '''
    p[0] = Selection(p[1], p[3])

def p_selection_path(p):
    ''' selection_path : NAME SELECTOR selection_path
                       | NAME '''
    
    if len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Build the parser
parser = yacc.yacc(write_tables=0, debug=0)
