from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class AccesoArreglo(Expresion):
    def __init__(self,id,expre, line, column):
        Expresion.__init__(self,line, column)
        self.id = id
        self.acceso = expre

    def compilar(self, enviroment:Enviroment):
        try:
            aux = Generator()
            generador = aux.getInstance()
            variable = enviroment.getVariable(self.id)
            if variable is None:
                print("el arreglo no existe")
                return Return(0,Type.INT)
            
            ret:Return = self.acceso[0].compilar(enviroment)
            if ret.tipo!=Type.INT:
                print("Expresion de acceso a arreglo invalida")
                return Return(0,Type.INT)
            

            posicionArreglo = generador.addTemporal()
            posicion = variable.posicion
            if not(variable.globalVar):
                posicion = generador.addTemporal()
                generador.addExpresion('P',variable.posicion,'+',posicion)
            generador.getStack(posicionArreglo,posicion)

            tempTamano = generador.addTemporal()
            labelError = generador.newLabel()
            salida = generador.newLabel()
            labelContinue = generador.newLabel()
            generador.getHeap(tempTamano,posicionArreglo)
            generador.addIf(ret.valor,tempTamano,'>',labelError)

            generador.addGoto(labelContinue)
            generador.putLabel(labelContinue)
            indiceAcceso = generador.addTemporal()
            generador.addExpresion(ret.valor,posicionArreglo,'+',indiceAcceso)
            tempReturn = generador.addTemporal()
            generador.getHeap(tempReturn,indiceAcceso)
            generador.addGoto(salida)

            generador.putLabel(labelError)
            generador.funcErrorArrego()
            generador.callFun("boundsError")
            generador.addExpresion('0','','',tempReturn)
            generador.addGoto(salida)

            generador.putLabel(salida)

            return Return(tempReturn,variable.tipoStruct,True)

        except:
            print("Error inesperado en acceso arreglo")
            return Return()
    
