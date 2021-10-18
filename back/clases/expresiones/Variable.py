from clases.abstract.Return import *
from clases.abstract.Expresion import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class LLamadaVariable(Expresion):
    def __init__(self,id, line, column):
        Expresion.__init__(self,line, column)
        self.id = id

    def compilar(self, enviroment:Enviroment):
        aux = Generator()
        generador = aux.getInstance()
        generador.addComent("LLamada Variable")

        variable = enviroment.getVariable(self.id)
        if variable==None:
            print("variable no existe")
            return Return()
        
        # temp para guardar variable
        temp = generador.addTemporal()
        posicion = variable.posicion
        if not(variable.globalVar):
            posicion = generador.addTemporal()
            generador.addExpresion('P',variable.posicion,'+',posicion)
        generador.getStack(temp,posicion)

        if variable.tipo == Type.INT or variable.tipo==Type.FLOAT:
            generador.addComent("Fin llamada Variable")
            return Return(temp,variable.tipo,True)
        elif variable.tipo==Type.BOOL:
            if self.trueLb=='':
                self.trueLb=generador.newLabel()
            if self.falseLb=='':
                self.falseLb=generador.newLabel()

            generador.addIf(temp,'1','==',self.trueLb)
            generador.addGoto(self.falseLb)    

            regreso = Return()
            regreso.tipo=Type.BOOL
            regreso.trueLb = self.trueLb
            regreso.falseLb = self.falseLb
            return regreso

        return Return()
        generador.addComent("Fin llamada Variable")


