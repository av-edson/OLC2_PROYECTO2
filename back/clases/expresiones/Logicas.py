from re import S
from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
from enum import Enum

class OperacionesLogicas(Enum):
    AND = 0
    OR = 1
    NOT = 2

class Logica(Expresion):
    def __init__(self,izquierdo,derecho,tipo, line, column):
        Expresion.__init__(self,line, column)
        self.izq = izquierdo
        self.der = derecho
        self.tipo = tipo

    def compilar(self, enviroment):
        aux = Generator()
        generator = aux.getInstance()

        generator.addComent("Inicio Expresion Logica")
        self.verLabels()
        lbAndOr = ''

        if self.tipo==OperacionesLogicas.AND:
            lbAndOr = self.izq.trueLb = generator.newLabel()
            self.der.trueLb = self.trueLb
            self.izq.falseLb = self.der.falseLb = self.falseLb
        elif self.tipo == OperacionesLogicas.OR:
            self.izq.trueLb = self.der.trueLb = self.trueLb
            lbAndOr = self.izq.falseLb = generator.newLabel()
            self.der.falseLb = self.falseLb
        else:
            self.izq.falseLb=self.trueLb
            self.izq.trueLb=self.falseLb
        
        izquierdo:Return = self.izq.compilar(enviroment)
        if izquierdo.tipo != Type.BOOL:
            print("solo se admiten booleanas en logicas")
            return
        if self.tipo==OperacionesLogicas.NOT:
            generator.addComent("Fin expresion logica")
            res = Return(0,Type.BOOL,False)
            res.trueLb = self.trueLb
            res.falseLb = self.falseLb
            return res
        generator.putLabel(lbAndOr)
        derecho = self.der.compilar(enviroment)
        if derecho.tipo != Type.BOOL:
            print("solo se admiten booleanas en logicas")
            return
        generator.addComent("Fin expresion logica")

        res = Return(0,Type.BOOL,False)
        res.trueLb = self.trueLb
        res.falseLb = self.falseLb
        return res


    def verLabels(self):
        aux = Generator()
        generator = aux.getInstance()
        if self.trueLb == '':
            self.trueLb = generator.newLabel()
        if self.falseLb == '':
            self.falseLb = generator.newLabel()
