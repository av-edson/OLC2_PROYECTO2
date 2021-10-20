from clases.abstract.Expresion import *
from clases.abstract.Return import Return, Type
from clases.enviroment.auxGenerador import auxGenerador
from clases.enviroment.Generator import Generator
from enum import Enum
from math import cos,sin,tan,sqrt,log,log10

class OpeNativas(Enum):
    LOGCOMUN=0
    LOGBASE=1
    SIN=2
    COS=3
    TAN=4
    RAIZ=5
    UPER=6
    LOWER=7
    LENGT=8
    POP=9

class ExpresionNativa(Expresion):
    def __init__(self,tipo,content, line, column,base=None):
        Expresion.__init__(self,line, column)
        self.tipo=tipo
        self.content=content
        self.base=base

    def compilar(self, enviroment):
        expre:Return = self.content.compilar(enviroment)
        if expre.tipo == Type.UNDEFINED:
            print("error en la expresion con funcion nativa")
            return Return()
        if self.base != None:
            base = self.base.ejecutar(enviroment)

        try:
            if self.tipo==OpeNativas.LOGCOMUN:
                return  self.log_comun(expre)
            elif self.tipo==OpeNativas.LOGBASE:
                return self.log_base(expre,base)
            elif self.tipo==OpeNativas.SIN:
                return self.seno(expre)
            elif self.tipo==OpeNativas.COS:
                return self.coseno(expre)
            elif self.tipo==OpeNativas.TAN:
                return self.tangente(expre)
            elif self.tipo==OpeNativas.RAIZ:
                return self.raiz(expre)
            elif self.tipo==OpeNativas.UPER:
                return self.uper(expre,enviroment)
            elif self.tipo==OpeNativas.LENGT:
                return self.length(expre,enviroment)
            elif self.tipo==OpeNativas.POP:
                return self.pop(expre,enviroment)
            else:
                return self.lower()
        except:
            print('----Error al ejecutar funcion nativa')
            return Return()

    def uper(self,expresion,enviroment):
        generador = auxGenerador()
        generador.Upper()
        retorno = generador.ge.addTemporal()
        generador.ge.addExpresion('H','2','-',retorno)
        generador.ge.getHeap(retorno,retorno)
        generador.ge.callFun("upper")
        return Return(retorno,Type.STRING,True)
    def lower(self):
        generador = auxGenerador()
        generador.Lower()
        retorno = generador.ge.addTemporal()
        generador.ge.addExpresion('H','2','-',retorno)
        generador.ge.getHeap(retorno,retorno)
        generador.ge.callFun("lower")
        return Return(retorno,Type.STRING,True)