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
