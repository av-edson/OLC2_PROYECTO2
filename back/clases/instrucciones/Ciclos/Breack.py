from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class Break(Instruccion):
    def __init__(self, line, column):
        Instruccion.__init__(self,line, column)
    
    def compilar(self, enviroment:Enviroment):
        if enviroment.lbBreack == '':
            print("Break fuera de ciclo")
            return
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addGoto(enviroment.lbBreack)