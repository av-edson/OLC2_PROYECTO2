
from analizadores.lexer import *
from clases.abstract.Return import Type
from clases.expresiones.Literal import ExpresionLiteral
from clases.expresiones.Aritmetica import OperacionAritmetica, OperacionesAritmeticas
from clases.instrucciones.Print import *
from clases.expresiones.Relacional import *
from clases.expresiones.Logicas import *

#------------------ SINTACTICO ---------------------------
precedence = (
    ('left','LOR'),
    ('left','LAND'),
    ('left','LNOT'),
    ('left','MAYOR','MENOR','MAYOR_IGUAL','MENOR_IGUAL','IGUAL_IGUAL','DIFERENTE'),
    ('left','SUMA','RESTA'),
    ('left','MULTI','DIV','MODULO'),
    ('left','POTENCIA'),
   # ('right','UMENOS'),
    ('left','PARENTESIS_IZQ','PARENTESIS_DER'),
)
def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]
def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]
def p_instruccion(t):
    '''instruccion  :   imprimir PUNTOCOMA'''
    t[0]=t[1]
def p_instruccion_error(t):
    '''instruccion  :   error PUNTOCOMA'''
    #errores.append(Error("Error sintactico en: '"+str(t[1].value)+"'",str(t.lineno(1)), str(t.lexpos(1)),str(time.strftime("%c"))))
    print('error en gramatica')
    t[0]=None

## -------------------------------- EXPRESIONES --------------------------
def p_expresion(t):
    '''expresion    :   expresion_bin
                    |   final_expresion'''
    t[0]=t[1]

def p_expresion_binaria(t):
    '''expresion_bin    :   expresion SUMA expresion
                            |   expresion RESTA expresion
                            |   expresion MULTI expresion
                            |   expresion DIV expresion
                            |   expresion MODULO expresion
                            |   expresion POTENCIA expresion'''
    if t.slice[2].type == "SUMA":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.SUMA,t.lineno(1),t.lexpos(0))
    elif t.slice[2].type == "RESTA":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.RESTA,t.lineno(1),t.lexpos(0))
    elif t.slice[2].type == "MULTI":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.MULTI,t.lineno(1),t.lexpos(0))
    elif t.slice[2].type == "DIV":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.DIV,t.lineno(1),t.lexpos(0))
    elif t.slice[2].type == "MODULO":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.MODULO,t.lineno(1),t.lexpos(0))
    elif t.slice[2].type == "POTENCIA":
        t[0] = OperacionAritmetica(t[1],t[3],OperacionesAritmeticas.POTENCIA,t.lineno(1),t.lexpos(0))

def p_expresion_relacional(t):
    '''expresion    :   expresion MAYOR expresion
                    |   expresion MENOR expresion
                    |   expresion MAYOR_IGUAL expresion
                    |   expresion MENOR_IGUAL expresion
                    |   expresion IGUAL_IGUAL expresion
                    |   expresion DIFERENTE expresion'''
    if t.slice[2].type=="MAYOR":
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.MAYOR,t.lineno(2),t.lexpos(2))
    elif t.slice[2].type=="MENOR":
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.MENOR,t.lineno(2),t.lexpos(2))
    elif t.slice[2].type=="MAYOR_IGUAL":
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.MAYOR_IGUAL,t.lineno(2),t.lexpos(2))
    elif t.slice[2].type=="MENOR_IGUAL":
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.MENOR_IGUAL,t.lineno(2),t.lexpos(2))
    elif t.slice[2].type=="IGUAL_IGUAL":
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.IGUAL_IGUAL,t.lineno(2),t.lexpos(2))
    else:
        t[0]=OperacionRelacional(t[1],t[3],TipoRelacional.DIFERENTE,t.lineno(2),t.lexpos(2))

def p_expresion_logica(t):
    '''expresion    :   LNOT expresion
                    |   expresion LOR expresion
                    |   expresion LAND expresion'''
    if t.slice[2].type=="LOR":
        t[0]=Logica(t[1],t[3],OperacionesLogicas.OR,t.lineno(2),t.lexpos(2))
    elif t.slice[2].type=="LAND":
        t[0]=Logica(t[1],t[3],OperacionesLogicas.AND,t.lineno(2),t.lexpos(2))
    elif t.slice[1].type=="LNOT":
        t[0]=Logica(t[2],None,OperacionesLogicas.NOT,t.lineno(1),t.lexpos(1))

def p_final_expresion(t):
    '''final_expresion  :   PARENTESIS_IZQ expresion PARENTESIS_DER
                        |   ENTERO
                        |   DECIMAL
                        |   CADENA
                        |   CARACTER
                        |   BOOLEANO
                        |   NULO
                        |   ID'''
    if len(t) == 2:
        if t.slice[1].type == "ENTERO":
            t[0] = ExpresionLiteral(Type.INT,int(t[1]),t.lineno(1),t.lexpos(0))
        elif t.slice[1].type == "DECIMAL":
            t[0] = ExpresionLiteral(Type.FLOAT,float(t[1]),t.lineno(1),t.lexpos(0))
        elif t.slice[1].type == "BOOLEANO":
            if str(t[1])=="true":
                t[0] = ExpresionLiteral(Type.BOOL,True,t.lineno(1),t.lexpos(0))
            else:
                t[0] = ExpresionLiteral(Type.BOOL,False,t.lineno(1),t.lexpos(0))
        elif t.slice[1].type == "CARACTER":
            t[0] = ExpresionLiteral(Type.CHAR,str(t[1]),t.lineno(1),t.lexpos(0))
        elif t.slice[1].type == "CADENA":
            t[0] = ExpresionLiteral(Type.STRING,str(t[1]),t.lineno(1),t.lexpos(0))
    else:
        t[0] = t[2]

def p_lista_expresiones(t):
    '''lista_expresiones    :   lista_expresiones COMA expresion'''  
    t[1].append(t[3])
    t[0] = t[1]
def p_lista_expresiones_expresion(t):
    '''lista_expresiones    :   expresion'''
    t[0] = [t[1]]

# ----------------------------- IMPRIMIR -------------------------
def p_imprimir(t):
    '''imprimir :   IMPRIMIR PARENTESIS_IZQ lista_expresiones PARENTESIS_DER
                |   IMPRIMIR_ML PARENTESIS_IZQ lista_expresiones PARENTESIS_DER
                |   IMPRIMIR_ML PARENTESIS_IZQ  PARENTESIS_DER
                |   IMPRIMIR PARENTESIS_IZQ  PARENTESIS_DER'''
    if t.slice[1].type=="IMPRIMIR":
        if len(t)==5:
            t[0]=Imprimir(t[3],TipoImpresion.PRINT,t.lineno(1),t.lexpos(1))
        else:
            t[0]=Imprimir([],TipoImpresion.PRINT,t.lineno(1),t.lexpos(1))
    else:
        if len(t)==5:
            t[0]=Imprimir(t[3],TipoImpresion.PRINTLN,t.lineno(1),t.lexpos(1))
        else:
            t[0]=Imprimir([],TipoImpresion.PRINTLN,t.lineno(1),t.lexpos(1))

                
import ply.yacc as yacc

def compilar(contenido):
    nuevoLexer()
    parser = yacc.yacc()
    return parser.parse(contenido)