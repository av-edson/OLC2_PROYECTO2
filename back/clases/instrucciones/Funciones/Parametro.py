from clases.abstract.Instruccion import Instruccion

class Parametro(Instruccion):
    def __init__(self,id,tipo, line, column,aux=None):
        Instruccion.__init__(self,line, column)
        self.id = id
        self.tipo = tipo
        self.tipoAux = aux

    def compilar(self, enviroment):
        return self