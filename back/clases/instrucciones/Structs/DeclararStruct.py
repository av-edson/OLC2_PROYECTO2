from clases.abstract.Instruccion import *
from clases.abstract.Return import Type
from clases.enviroment.Enviroment import Enviroment

class DeclararStruct(Instruccion):
    def __init__(self, id, tipo, line, column):
        Instruccion.__init__(self, line, column)
        self.id = id
        self.tipo = tipo
    
    def compilar(self, environment:Enviroment):
        environment.sabeVar(self.id,Type.STRUCT,True,self.tipo,True)