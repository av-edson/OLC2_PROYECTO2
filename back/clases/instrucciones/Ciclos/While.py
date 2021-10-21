from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class WhileST(Instruccion):
    def __init__(self,expresion,instrucciones, line, column):
        Instruccion.__init__(self,line, column)
        self.expresione = expresion
        self.instrucciones = instrucciones

    def compilar(self, enviroment:Enviroment):
        aux = Generator()
        generador = aux.getInstance()
        generador.addComent("Inicio ciclo while")
        labelCiclo = generador.newLabel()
        generador.putLabel(labelCiclo)
    
        expresion:Return = self.expresione.compilar(enviroment)
        if expresion.tipo != Type.BOOL:
            print("Expresion del while no es booleana")
            generador.addComent("Fin ciclo while")
            return
        entornoInterno:Enviroment = Enviroment(enviroment,"Ciclo While-"+str(self.line))

        entornoInterno.lbBreack = expresion.falseLb
        entornoInterno.lbContinue = labelCiclo

        generador.putLabel(expresion.trueLb)
        self.instrucciones.compilar(entornoInterno)
        generador.addGoto(labelCiclo)

        generador.putLabel(expresion.falseLb)
        generador.addComent("Fin ciclo while")
        return