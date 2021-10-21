from clases.abstract.Expresion import Expresion
from clases.abstract.Return import Return, Type
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class ReturnST(Expresion):
    def __init__(self,expresion, line, column):
        Expresion.__init__(self,line, column)
        self.expresion = expresion
    
    def compilar(self, enviroment:Enviroment):
        if (enviroment.lbReturn == ""):
            print("Return fuera de funcion")
            return

        aux = Generator()
        generador = aux.getInstance()
        #if self.expresion is None:
        #    ret = Return(0,Type.INT)
        #    return ret
        ret:Return = self.expresion.compilar(enviroment)
        if ret.tipo==Type.INT or ret.tipo==Type.FLOAT:
            generador.setStack('P',ret.valor)
        elif ret.tipo==Type.BOOL:
            temporarLabel = generador.newLabel()

            generador.putLabel(ret.trueLb)
            generador.setStack('P','1')
            generador.addGoto(temporarLabel)

            generador.putLabel(ret.falseLb)
            generador.setStack('P','0')
            generador.putLabel(temporarLabel)
        else:
            print(" error o no se implemente")
        generador.addGoto(enviroment.lbReturn)
