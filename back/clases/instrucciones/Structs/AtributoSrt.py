from clases.abstract.Instruccion import *

class AtrStruct(Instruccion):
    def __init__(self, id, tipo, line, column):
        Instruccion.__init__(self, line, column)
        self.id = id
        self.tipo = tipo
    
    def compilar(self, environment):
        return self