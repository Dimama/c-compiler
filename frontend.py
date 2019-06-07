import ply.yacc as yacc
import ply.lex as lex

# Reserved words
reserved = \
    ('BREAK', 'CHAR', 'CONTINUE', 'DO', 'ELSE', 'FOR', 'IF', 'INT', 'RETURN', 'VOID', 'WHILE', 'ASM', 'PRINTSTR')

tokens = reserved + (
    'ID', 'NUMBER', 'S_CONST', 'C_CONST',

    # Operators (||, &&, <=, >=, ==, !=)
    'LOR', 'LAND',
    'LE', 'GE', 'EQ', 'NE',

    # Assignment (*=, /=, +=, -=, &=, ^=, |=)
    'TIMESEQUAL', 'DIVEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    'PLUSPLUS', 'MINUSMINUS',

)

literals = ['=', '+', '-', '*', '/', '&', '|', '^', '~', '(', ')', '{', '}',
            '[', ']', ';', ',', '!', '<', '>']

# Tokens

# Operators
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Assignment operators

t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='

# Increment/decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# String literal
t_S_CONST = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'text'
t_C_CONST = r'(L)?\'([^\\\n]|(\\.))*?\''

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_ID(t):
    r"""[A-Za-z_][\w_]*"""
    t.type = reserved_map.get(t.value, "ID")
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_comment(t):
    r"""/\*(.|\n)*?\*/"""
    t.lexer.lineno += t.value.count('\n')


def t_comment2(t):
    r"""\/\/([^\\\n])*?\n"""
    t.lexer.lineno += t.value.count('\n')


def t_preprocessor(t):
    r"""\#(.)*?\n"""
    t.lexer.lineno += 1


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lex.lex()

# Parsing rules
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def p_file(p):
    """file : unit
            | file unit"""
    if len(p) >= 3:
        p[0] = ('unit', p[1], p[2])
    else:
        p[0] = p[1]


def p_unit(p):
    """unit : fun_def
            | declaration ";" """
    p[0] = p[1]


def p_statement_fun_def(p):
    """fun_def : declaration_specifier ID "(" ")" compound_statement
               | declaration_specifier ID "(" declaration_list ")" compound_statement"""
    if len(p) >= 7:
        p[0] = ('fun', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('fun', p[1], p[2], p[5])


def p_statement_expr(p):
    """statement : expression ";"
                 | declaration ";"
                 | compound_statement"""
    p[0] = p[1]


def p_statement_fun_call(p):
    """expression : ID "(" ")"
                  | ID "(" expression_list ")" """
    if len(p) > 4:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1])


def p_statement_asm_call(p):
    """expression : ASM "(" S_CONST ")" """
    p[0] = (p[1], p[3])


def p_statement_str_call(p):
    """expression : PRINTSTR "(" S_CONST ")" """
    p[0] = (p[1], p[3])


def p_declaration_specifier(p):
    """declaration_specifier : VOID
                             | INT
                             | CHAR
                             | INT pointer
                             | CHAR pointer"""
    if len(p) >= 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_statement_return(p):
    """statement : RETURN expression ";"
                 | RETURN ";" """
    if len(p) >= 4:
        p[0] = ("ret", p[2])
    else:
        p[0] = ("ret",)


def p_statement_break(p):
    """statement : BREAK ";" """
    p[0] = ('break',)


def p_statement_continue(p):
    """statement : CONTINUE ";" """
    p[0] = ('continue',)


def p_statement_while_def(p):
    """statement : WHILE "(" expression ")" statement"""
    p[0] = ('while', p[3], p[5])


def p_statement_dowhile_def(p):
    """statement : DO statement WHILE "(" expression ")" ";" """
    p[0] = ('dowhile', p[5], p[2])


def p_statement_for_def(p):
    """statement : FOR "(" expression ";" expression ";" expression ")" statement"""
    p[0] = ('for', p[3], p[5], p[7], p[9])


def p_statement_if_def(p):
    """statement : IF "(" expression ")" statement"""
    p[0] = ('if', p[3], p[5])


def p_statement_if_else_def(p):
    """statement : IF "(" expression ")" statement ELSE statement"""
    p[0] = ('ifelse', p[3], p[5], p[7])


def p_statement_arr_def(p):
    """declaration : declaration_specifier ID "[" NUMBER "]" "=" "{" expression_list "}"
                   | declaration_specifier ID "[" NUMBER "]" """
    if len(p) <= 7:
        p[0] = ('arrdeciz', p[1], p[2], p[4])
    else:
        p[0] = ('arrdeci', p[1], p[2], p[4], p[8])


def p_statement_def(p):
    """declaration : declaration_specifier ID "=" expression
                   | declaration_specifier ID """
    if len(p) >= 5:
        p[0] = ('decli', p[1], p[2], p[4])
    else:
        p[0] = ('decli', p[1], p[2])


def p_statement_rminusminus(p):
    """expression : MINUSMINUS ID"""
    p[0] = (('assign', p[2], ('binop', '-', ('id', p[2]), '1')), ('id', p[2]))


def p_statement_minusminus(p):
    """expression : ID MINUSMINUS"""
    p[0] = (('id', p[1]), ('assign', p[1], ('binop', '-', ('id', p[1]), '1')))


def p_statement_rplusplus(p):
    """expression : PLUSPLUS ID """
    p[0] = (('assign', p[2], ('binop', '+', ('id', p[2]), '1')), ('id', p[2]))


def p_statement_plusplus(p):
    """expression : ID PLUSPLUS """
    p[0] = (('id', p[1]), ('assign', p[1], ('binop', '+', ('id', p[1]), '1')))


def p_statement_xoreq(p):
    """expression : ID XOREQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '^', ('id', p[1]), p[3]))


def p_statement_andeq(p):
    """expression : ID ANDEQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '&', ('id', p[1]), p[3]))


def p_statement_oreq(p):
    """expression : ID OREQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '|', ('id', p[1]), p[3]))


def p_statement_muleq(p):
    """expression : ID TIMESEQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '*', ('id', p[1]), p[3]))


def p_statement_diveq(p):
    """expression : ID DIVEQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '/', ('id', p[1]), p[3]))


def p_statement_pluseq(p):
    """expression : ID PLUSEQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '+', ('id', p[1]), p[3]))


def p_statement_minuseq(p):
    """expression : ID MINUSEQUAL expression"""
    p[0] = ('assign', p[1], ('binop', '-', ('id', p[1]), p[3]))


def p_statement_assign(p):
    """expression : ID "=" expression"""
    p[0] = ('assign', p[1], p[3])


def p_expression_list(p):
    """expression_list : expression
                       | expression_list ',' expression"""
    if len(p) >= 3:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]


def p_declaration_list(p):
    """declaration_list : declaration
                        | declaration_list ',' declaration"""
    if len(p) >= 3:
        p[0] = (p[1], p[3])
    else:
        p[0] = p[1]


def p_expression_binop(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '&' expression
                  | expression '|' expression
                  | expression '^' expression"""
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_not(p):
    """expression : '~' expression %prec UMINUS"""
    p[0] = ('not', p[2])


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = ('uminus', p[2])


def p_expression_group(p):
    """expression : '(' expression ')' """
    p[0] = p[2]


def p_expression_arr_name(p):
    """expression : ID '[' expression ']'"""
    p[0] = ('arrid', p[1], p[3])


def p_expression_arr_assign(p):
    """expression : ID '[' expression ']' '=' expression"""
    p[0] = ('arrassign', p[1], p[3], p[6])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_name(p):
    """expression : ID"""
    p[0] = ('id', p[1])


def p_expression_address(p):
    """expression : '&' ID"""
    p[0] = ('address', p[2])


def p_expression_arr_address(p):
    """expression : '&' ID '[' expression ']' """
    p[0] = ('arraddress', p[2], p[4])


def p_statement_ptr_assign(p):
    """expression : "*" ID "=" expression"""
    p[0] = ('passign', p[2], p[4])


def p_expression_pointer_access(p):
    """expression : '*' ID"""
    p[0] = ('paccess', p[2])


def p_expression_pointer(p):
    """pointer : '*'
               | pointer '*' """
    if len(p) >= 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_expression_char(p):
    """expression : C_CONST"""
    p[0] = ('char', p[1])


def p_cond_exp(p):
    """expression : eq_exp"""
    p[0] = p[1]


def p_eq_exp(p):
    """eq_exp : expression EQ expression
              | expression NE expression
              | expression LOR expression
              | expression LAND expression
              | expression '<' expression
              | expression '>' expression
              | expression GE expression
              | expression LE expression"""
    p[0] = ('cond', p[2], p[1], p[3])


def p_compound_statement(p):
    """compound_statement : "{" statement_list "}"
                          | "{" "}" """
    if len(p) >= 4:
        p[0] = p[2]


def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement"""
    if len(p) >= 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_error(p):
    if p:
        print(f"Syntax error at: {p.value} line: {str(p.lineno)}")
    else:
        print("Syntax error at EOF")


yacc.yacc()
