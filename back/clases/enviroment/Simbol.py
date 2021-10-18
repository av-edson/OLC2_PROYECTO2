from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *

class Simbolo:

    def __init__(self,identificador,tipo,posicion,globalVar,inHeap,strucTipo=None):
        self.simbolId=identificador
        self.tipo:Type=tipo
        self.posicion=posicion
        self.globalVar = globalVar
        self.inHeap = inHeap
        self.tipoStruct = strucTipo
        self.value = None
       