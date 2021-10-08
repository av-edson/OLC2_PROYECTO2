from clases.enviroment.Generator import Generator
from clases.abstract.Return import *
from clases.abstract.Instruccion import Instruccion
from enum import Enum

class TipoImpresion(Enum):
    PRINT=0
    PRINTLN=1

class Imprimir(Instruccion):
    def __init__(self,listaExpresiones,tipo, line, column):
        Instruccion.__init__(self,line, column)
        self.tipo=tipo
        self.listaExpre = listaExpresiones
    def compilar(self, enviroment):
        try:
            lista = []
            for exp in self.listaExpre:
                res:Return = exp.compilar(enviroment)
                if res.tipo == Type.UNDEFINED:
                    print("una de las expresiones en el print tiene error")
                    return
                # ver los demas tipos de datos
                lista.append(res)   
            if self.tipo==TipoImpresion.PRINT:
                self.ImprimirSimple(lista)
        except:
            print("error inesperado en el print")
        
    def ImprimirSimple(self,lista):
        genAux = Generator()
        generador = genAux.getInstance()
        for expre in lista:
            if expre.tipo == Type.INT:
                generador.addPrint("d",expre.valor)
        generador.addPrint(None,None)
    
    def ImprimirML(self, lista):
        genAux = Generator()
        generador = genAux.getInstance()
        for expre in lista:
            if expre.tipo == Type.INT:
                generador.addPrint("d",expre.valor)
                generador.addPrint(None,None)
