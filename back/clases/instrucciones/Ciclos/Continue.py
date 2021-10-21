from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class Continue(Instruccion):

    def __init__(self, line, column):
        Instruccion.__init__(self,line, column)
    
    def compilar(self, enviroment:Enviroment):
        if enviroment.lbContinue == '':
            print("Continue declarado fuera de ciclo")
            return
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addGoto(enviroment.lbContinue)