from enum import Enum
from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
class OperacionesAritmeticas(Enum):
    SUMA = 0
    RESTA = 1
    MULTI = 2
    DIV = 3

class OperacionAritmetica(Expresion):
    def __init__(self,izquierdo,derecho,tipo, line, column):
        Expresion.__init__(self,line, column)
        self.izquierdo=izquierdo
        self.derecho=derecho
        self.tipo=tipo

    def compilar(self, enviroment):
        # obteniendo generador
        aux = Generator()
        generador = aux.getInstance()
        # compilando valores
        try:
            der=self.derecho.compilar(enviroment)
            izq=self.izquierdo.compilar(enviroment)
            ope = ""
            res = Return()

            if(self.tipo==OperacionesAritmeticas.SUMA):
                res = self.suma(izq,der)
                if res == None: return Return()
                ope="+"
            elif (self.tipo==OperacionesAritmeticas.RESTA):
                ope="-"
            elif (self.tipo==OperacionesAritmeticas.MULTI):
                ope="*"
            elif (self.tipo==OperacionesAritmeticas.DIV):
                ope="/"
            temp = generador.addTemporal()
            generador.addExpresion(izq.valor,der.valor,ope,temp)
            return res
        except:
            print("error inesperado en la operacion binaria")
    
    def suma(self,izq,der):
        return False

