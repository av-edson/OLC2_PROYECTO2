from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *

class ExpresionLiteral(Expresion):
    def __init__(self,tipoDato,valorDato, line, column):
        Expresion.__init__(self,line,column)
        self.tipo=tipoDato # regresa el tipo de dato de la expresion
        self.valor=valorDato
    
    def compilar(self, enviroment):
        if (self.tipo==Type.INT or self.tipo==Type.FLOAT):
            return Return(self.valor,self.tipo)
        else:
            print('falta culo')

