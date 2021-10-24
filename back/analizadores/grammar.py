
from analizadores.lexer import *
from clases.abstract.Return import Type
from clases.expresiones.Literal import ExpresionLiteral
from clases.expresiones.Aritmetica import OperacionAritmetica, OperacionesAritmeticas
from clases.instrucciones.Arreglos.AccesoArr import AccesoArreglo
from clases.instrucciones.Funciones.Funcion import Funcion
from clases.instrucciones.Funciones.LLamadaFuncion import LLamadaFuncion
from clases.instrucciones.Funciones.Parametro import Parametro
from clases.instrucciones.Funciones.Return import ReturnST
from clases.instrucciones.Print import *
from clases.expresiones.Relacional import *
from clases.expresiones.Logicas import *
from clases.expresiones.Variable import *
from clases.instrucciones.Declaracion import Declaracion
from clases.expresiones.Nativas import *
from clases.instrucciones.Condicionales.SentenciaIf import If
from clases.instrucciones.BloqueInstrucciones import BloqueInstrucciones
from clases.instrucciones.Ciclos.While import WhileST
from clases.instrucciones.Ciclos.Breack import Break
from clases.instrucciones.Ciclos.Continue import Continue
from clases.instrucciones.Ciclos.ForSt import CicloFor
from clases.instrucciones.Arreglos.DeclaracionArreglo import DeclaracionArreglo

#------------------ SINTACTICO ---------------------------
precedence = (
    ('left','LOR'),
    ('left','LAND'),
    ('left','LNOT'),
    ('left','MAYOR','MENOR','MAYOR_IGUAL','MENOR_IGUAL','IGUAL_IGUAL','DIFERENTE'),
    ('left','SUMA','RESTA'),
    ('left','MULTI','DIV','MODULO'),
    ('left','POTENCIA'),
    ('right','UMENOS'),
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
    '''instruccion  :   imprimir PUNTOCOMA
                    |   declaracion PUNTOCOMA
                    |   sentencia_if PUNTOCOMA
                    |   sentencia_while PUNTOCOMA
                    |   salto_control PUNTOCOMA
                    |   sentencia_for PUNTOCOMA
                    |   declaracion_funcion PUNTOCOMA
                    |   llamada_funcion PUNTOCOMA
                    |   returnST PUNTOCOMA'''
    t[0]=t[1]

def p_bloque_instrucciones(t):
    '''bloque_instrucciones :   instrucciones'''
    t[0] = BloqueInstrucciones(t[1],t.lineno(1),t.lexpos(0))

def p_instruccion_error(t):
    '''instruccion  :   error PUNTOCOMA'''
    #errores.append(Error("Error sintactico en: '"+str(t[1].value)+"'",str(t.lineno(1)), str(t.lexpos(1)),str(time.strftime("%c"))))
    print('error en gramatica')
    t[0]=None

## -------------------------------- EXPRESIONES --------------------------
def p_expresion(t):
    '''expresion    :   RESTA expresion %prec UMENOS
                    |   expresion_bin
                    |   final_expresion'''
    if t.slice[1].type=="RESTA":
        t[0] = OperacionAritmetica(ExpresionLiteral(Type.INT,int(-1),t.lineno(1),t.lexpos(0))
        ,t[2],OperacionesAritmeticas.MULTI,t.lineno(1),t.lexpos(0))
    else:
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

def p_expresion_funcion_nativa(t):
    '''expresion    :   FLOG10 PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FLOG PARENTESIS_IZQ expresion COMA expresion PARENTESIS_DER
                    |   FSIN PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FCOS PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FTAN PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FSQRT PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   UPERCASE PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   LOWERCASE PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FLENGTH PARENTESIS_IZQ expresion PARENTESIS_DER
                    |   FPOP LNOT PARENTESIS_IZQ expresion PARENTESIS_DER'''
    if t.slice[1].type=="FLOG10":
        t[0]=ExpresionNativa(OpeNativas.LOGCOMUN,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FLOG":
        t[0]=ExpresionNativa(OpeNativas.LOGBASE,t[5],t.lineno(1),t.lexpos(1),t[3])
    elif t.slice[1].type=="FSIN":
        t[0]=ExpresionNativa(OpeNativas.SIN,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FCOS":
        t[0]=ExpresionNativa(OpeNativas.COS,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FTAN":
        t[0]=ExpresionNativa(OpeNativas.TAN,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FSQRT":
        t[0]=ExpresionNativa(OpeNativas.RAIZ,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="UPERCASE":
        t[0]=ExpresionNativa(OpeNativas.UPER,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FLENGTH":
        t[0]=ExpresionNativa(OpeNativas.LENGT,t[3],t.lineno(1),t.lexpos(1))
    elif t.slice[1].type=="FPOP":
        t[0]=ExpresionNativa(OpeNativas.POP,t[4],t.lineno(1),t.lexpos(1))
    else:
        t[0]=ExpresionNativa(OpeNativas.LOWER,t[3],t.lineno(1),t.lexpos(1))

def p_final_expresion(t):
    '''final_expresion  :   llamada_funcion
                        |   PARENTESIS_IZQ expresion PARENTESIS_DER
                        |   ENTERO
                        |   DECIMAL
                        |   CADENA
                        |   CARACTER
                        |   BOOLEANO
                        |   NULO
                        |   ID
                        |   lista_array
                        |   accesoArreglo'''
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
        elif t.slice[1].type=="ID":
            t[0] = LLamadaVariable(str(t[1]),t.lineno(1),t.lexpos(0))
        else: 
            t[0]=t[1]
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

# ------------------------------ DECLARACION ----------------
def p_declaracion(t):
    '''declaracion   :  ID IGUAL expresion  
                    |   ID IGUAL expresion DOSPUNTOS DOSPUNTOS tipodato'''
    if len(t)==7:
        t[0]=Declaracion(t[1],t[3],t.lineno(1),t.lexpos(1),False,t[6])
    else:
        t[0]=Declaracion(t[1],t[3],t.lineno(1),t.lexpos(1))

# ------------------------ FALTA LA 2DA PARTE DE LOCAL Y GLOBAL
def p_modificar_declaracion(t):
    '''declaracion  :   LOCAL declaracion
                    |   VGLOBAL declaracion'''
    if t.slice[1].type=="LOCAL":
        t[2].esGlobal = False
        t[0] = t[2]
    else:
        t[2].esGlobal = True
        t[0] = t[2]

def p_salto_control(t):
    '''salto_control :   CONTINUEST
                    |   BREACKST'''
    if t.slice[1].type=="CONTINUEST":
            t[0] = Continue(t.lineno(1),t.lexpos(0))
    elif t.slice[1].type=="BREACKST":
        t[0] = Break(t.lineno(1),t.lexpos(0))      

def p_sentencia_for(t):
    '''sentencia_for    :   FORST ID EIN expresion DOSPUNTOS expresion bloque_instrucciones FIN
                        |   FORST ID EIN expresion bloque_instrucciones FIN'''
    if len(t)==9:
        t[0]=CicloFor(t[2],t[4],t[7],t.lineno(1), t.lexpos(1),t[6])

def p_tipodato(t):
    '''tipodato :   DINT64 
                    |   DFLOAT64 
                    |   DBOOL 
                    |   DSTRING 
                    |   DCHAR 
                    |   STRUCT'''    
    if t.slice[1].type=='DINT64':
        t[0]=Type.INT
    elif t.slice[1].type=='DFLOAT64':
        t[0]=Type.FLOAT
    elif t.slice[1].type=='DBOOL':
        t[0]=Type.BOOL
    elif t.slice[1].type=='DSTRING':
        t[0]=Type.STRING
    elif t.slice[1].type=='DCHAR':
        t[0]=Type.CHAR
    elif t.slice[1].type=='STRUCT':
        t[0]=Type.STRUCT

#-------------------------------------- CONDICIONALES ------------------------------------

def p_sentencia_if(t):
    '''sentencia_if  : IFST  expresion bloque_instrucciones  FIN
                    | IFST expresion bloque_instrucciones ELSEST bloque_instrucciones  FIN
                    | IFST expresion bloque_instrucciones elif_lista FIN'''
    if len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0))
    elif len(t) == 7:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[5])
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[4])

def p_elseIfList(t):
    '''elif_lista   : ELIFST expresion bloque_instrucciones
                    | ELIFST expresion bloque_instrucciones ELSEST bloque_instrucciones
                    | ELIFST expresion bloque_instrucciones elif_lista'''
    if len(t) == 4:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0))
    elif len(t) == 6:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[5])
    elif len(t) == 5:
        t[0] = If(t[2], t[3], t.lineno(1), t.lexpos(0), t[4])

# ------------------------------------ CICLOS -------------------------------------------
def p_sentencia_while(t):
    '''sentencia_while  :   WHILEST expresion bloque_instrucciones FIN'''
    t[0] = WhileST(t[2],t[3],t.lineno(1), t.lexpos(1))

def p_sentencia_for(t):
    '''sentencia_for    :   FORST ID EIN expresion DOSPUNTOS expresion bloque_instrucciones FIN
                        |   FORST ID EIN expresion bloque_instrucciones FIN'''
    if len(t)==9:
        t[0]=CicloFor(t[2],t[4],t[7],t.lineno(1), t.lexpos(1),t[6])
    else:
        t[0]=CicloFor(t[2],t[4],t[5],t.lineno(1), t.lexpos(1))

# --------------------------------- FUNCIONES --------------------------------------------
def p_declaracion_funcion(t):
    '''declaracion_funcion  :   FUNCION ID PARENTESIS_IZQ params_function PARENTESIS_DER bloque_instrucciones FIN
                            |   FUNCION ID PARENTESIS_IZQ PARENTESIS_DER bloque_instrucciones FIN
                            |   FUNCION ID PARENTESIS_IZQ params_function PARENTESIS_DER DOSPUNTOS DOSPUNTOS tipodato bloque_instrucciones FIN
                            |   FUNCION ID PARENTESIS_IZQ PARENTESIS_DER DOSPUNTOS DOSPUNTOS tipodato bloque_instrucciones FIN''' 
    if len(t)==7:
        t[0] = Funcion(t[2],t[5],[],None,t.lineno(1), t.lexpos(1))
    elif len(t)==8:
        t[0] = Funcion(t[2],t[6],t[4],None,t.lineno(1), t.lexpos(1))
    elif len(t)==11:
        t[0] = Funcion(t[2],t[9],t[4],t[8],t.lineno(1), t.lexpos(1))
    else:
        t[0] = Funcion(t[2],t[8],[],t[7],t.lineno(1), t.lexpos(1))

def p_params_funcion(t):
    '''params_function  :   params_function COMA ID DOSPUNTOS DOSPUNTOS tipodato
                        |   ID DOSPUNTOS DOSPUNTOS tipodato'''
    if len(t)==2:
        t[0] = [Parametro(t[1],None, t.lineno(1), t.lexpos(1))]
    elif len(t)==4:
        t[1].append(Parametro(t[3],None, t.lineno(3), t.lexpos(3)))
        t[0] = t[1]
    elif len(t)==5:
        t[0] = [Parametro(t[1],t[4], t.lineno(1), t.lexpos(1))]
    else:
        t[1].append(Parametro(t[3],t[6], t.lineno(3), t.lexpos(3)))
        t[0] = t[1]

def p_llamada_funcion(t):
    '''llamada_funcion  :   ID PARENTESIS_IZQ PARENTESIS_DER
                        |   ID PARENTESIS_IZQ lista_expresiones PARENTESIS_DER
                        |   FPUSH LNOT PARENTESIS_IZQ lista_expresiones PARENTESIS_DER'''
    if len(t)==4:
        t[0] = LLamadaFuncion(t[1],[],t.lineno(1), t.lexpos(1))
    else:
        t[0] = LLamadaFuncion(t[1],t[3],t.lineno(1), t.lexpos(1))

def p_return(t):
    '''returnST :   RETURNST expresion
                    |   RETURNST'''
    if len(t) == 2:
        t[0] = ReturnST(None, t.lineno(1), t.lexpos(1))
    else:
        t[0] = ReturnST(t[2], t.lineno(1), t.lexpos(1))

# ---------------------------------- ARREGLOS -----------------------------------------------
def p_lista_array(t):
    '''lista_array  : COR_ABRE lista_expresiones COR_CIERRA'''
    t[0]=DeclaracionArreglo(t[2],t.lineno(1),t.lexpos(0))

def p_accesoArreglo(t):
    '''accesoArreglo    :   ID listaAcceso_arreglo'''
    t[0]=AccesoArreglo(t[1],t[2],t.lineno(1),t.lexpos(1))

def p_listaAcceso_arreglo(t):
    '''listaAcceso_arreglo  :   listaAcceso_arreglo COR_ABRE expresion COR_CIERRA
                            |   COR_ABRE expresion COR_CIERRA'''
    if len(t)==4:
        t[0] = [t[2]]
    else:
        t[1].append(t[3])
        t[0]=t[1]

import ply.yacc as yacc

def compilar(contenido):
    nuevoLexer()
    parser = yacc.yacc()
    return parser.parse(contenido)
