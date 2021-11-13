from clases.abstract.Instruccion import *
from clases.enviroment.Enviroment import Enviroment
class CreateStruct(Instruccion):

    def __init__(self, id, atributos, line, column,mutable=False):
        Instruccion.__init__(self, line, column)
        self.id = id
        self.atributos = atributos
        self.mutable=mutable
    
    def compilar(self, environment:Enviroment):
        environment.saveStruct(self.id, self)