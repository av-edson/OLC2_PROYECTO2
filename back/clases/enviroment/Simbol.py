from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *

class Simbolo:

    def __init__(self,identificador,posicion,globalVar,inHeap,tipo=None,fila=None,columna=None,):
        self.simbolId=identificador
        self.tipo:Type=tipo
        self.fila = fila
        self.columna = columna
        self.posicion=posicion
        self.globalVar = globalVar
        self.inHeap = inHeap

        self.value = None
       