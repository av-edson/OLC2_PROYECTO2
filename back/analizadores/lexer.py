#from controller import consola
#from clases.error import Error
import time
errores=[]
listaStructs=[]
esStruct = False
reservadas = {
    'log10' : 'FLOG10',
    'log' : 'FLOG',
    'sin':'FSIN',
    'cos':'FCOS',
    'tan':'FTAN',
    'sqrt':'FSQRT',
    'uppercase':'UPERCASE',
    'lowercase':'LOWERCASE',
    'Int64':'DINT64',
    'Float64':'DFLOAT64',
    'Bool':'DBOOL',
    'Char':'DCHAR',
    'String':'DSTRING',
    'Array':'DARRAY',
    'nothing':'NULO',
    'true':'BOOLEANO',
    'false':'BOOLEANO',
    'print':'IMPRIMIR',
    'println':'IMPRIMIR_ML',
    'parse':'FPARSE',
    'trunc':'FTRUNC',
    'float':'FFLOAT',
    'typeof':'FTYPEOF',
    'string':'FSTRING',
    'push':'FPUSH',
    'pop':'FPOP',
    'length':'FLENGTH',
    'local':'LOCAL',
    'global':'VGLOBAL',
    'function':'FUNCION',
    'end':'FIN',
    'return':'RETURNST',
    'if':'IFST',
    'else':'ELSEST',
    'elseif':'ELIFST',
    'while':'WHILEST',
    'continue':'CONTINUEST',
    'break':'BREACKST',
    'for':'FORST',
    'in':'EIN',
    'struct':'STRUCT',
    'mutable':'MUTABLE',
}

tokens = [
    'COMENTARIOSIMPLE',
    'COMENTARIOMULTIPLE',
    # AGRUPACION
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'COR_ABRE',
    'COR_CIERRA',
    'LLA_ABRE',
    'LLA_CIERRA',
    # ARITMETICAS
    'SUMA',
    'RESTA',
    'MULTI',
    'DIV',
    'POTENCIA',
    'MODULO',
    # RELACIONALES 
    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'IGUAL_IGUAL',
    'DIFERENTE',
    # LOGICAS
    'LOR' ,
    'LAND',
    'LNOT',
    # DATOS
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'ID',
    'CARACTER',
    # otros
    'IGUAL',
    'PUNTOCOMA',
    'COMA',
    'DOSPUNTOS',
    'PUNTO',
] + list(reservadas.values())

# Tokens
t_LLA_CIERRA = r'\}'
t_LLA_ABRE = r'\{'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTI = r'\*'
t_DIV = r'\/'
t_POTENCIA = r'\^'
t_MODULO = r'\%'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_LOR = r'\|\|' 
t_LAND = r'&&'
t_LNOT = r'!'
t_IGUAL = r'\='
t_PUNTOCOMA = r'\;'
t_COMA = r'\,'
t_DOSPUNTOS = r'\:'
t_PUNTO  = r'\.'
t_COR_ABRE = r'\['
t_COR_CIERRA = r'\]'


#decimal
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t
# entero
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
# booleano
# cadena
def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] 
    return t 
    # CARACTER
def t_CARACTER(t):
    r'\'.*?\''
    t.value = t.value[1:-1] 
    return t 
#identificador
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID') 
     return t
# comentario multi linea
def t_COMENTARIOMULTIPLE(t):
    r'\#\=((.|\n)*)?\=\#'
    t.lexer.lineno += t.value.count("\n")
    pass
# comentario simple
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1
    pass
# ignorados
t_ignore = " \t"
#salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
# fin de documento
def t_eof(t):
    return None
# manejador de errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    # print(t.lexer.lineno) t.lexer.lineno t.lexer.value 
   # errores.append(Error("Caracter no esperado: '"+str(t.value[0])+"'",str(t.lexer.lineno),str(t.lexer.lexpos),str(time.strftime("%c"))))
    t.lexer.skip(1)

def buscarColumna(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex()
def nuevoLexer():
    global lexer
    lexer = lex.lex()