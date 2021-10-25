from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from clases.enviroment.Simbol import Simbolo

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
            generador.addComent("Inicio acceso arreglo")
            if variable is None:
                print("el arreglo no existe")
                return Return(0,variable.tipoStruct)
            
            listaValores = []
            for expre in self.acceso:
                ret:Return = expre.compilar(enviroment)
                if ret.tipo != Type.INT:
                    print('una de las expresiones dentro de la llamada arreglo no es entera')
                    return Return(0,Type.INT)
                listaValores.append(ret)
            
            listaValores.reverse()
            regreso = self.accesoArreglo(variable,listaValores.copy(),generador)
            return regreso
        except:
            print("Error inesperado en acceso arreglo")
            return Return()
    
    def accesoArreglo(self,arreglo:Simbolo,expresiones,generador:Generator):
        expreActual:Return = expresiones.pop()
        if expreActual.tipo!=Type.INT:
                print("Expresion de acceso a arreglo invalida")
                return Return(0,arreglo.tipoStruct)

        posicionArreglo = generador.addTemporal()
        posicion = arreglo.posicion

        returnAux = generador.addTemporal()
        generador.addExpresion('H','','',returnAux)

        if not(arreglo.globalVar):
            posicion = generador.addTemporal()
            generador.addExpresion('P',arreglo.posicion,'+',posicion)
        generador.getStack(posicionArreglo,posicion)

        tempTamano = generador.addTemporal()
        labelError = generador.newLabel()
        salida = generador.newLabel()
        labelContinue = generador.newLabel()

        generador.getHeap(tempTamano,posicionArreglo)
        generador.addIf(expreActual.valor,tempTamano,'>',labelError)
        generador.addGoto(labelContinue)

        generador.putLabel(labelContinue)
        indiceAcceso = generador.addTemporal()
        generador.addExpresion(expreActual.valor,posicionArreglo,'+',indiceAcceso)
        tempReturn = generador.addTemporal()
        generador.getHeap(tempReturn,indiceAcceso)
        generador.addGoto(salida)

        generador.putLabel(labelError)
        generador.funcErrorArrego()
        generador.callFun("boundsError")
        generador.addExpresion('0','','',tempReturn)
        generador.addGoto(salida)
        generador.putLabel(salida)

        if len(expresiones) !=0:
            return self.buscarEnArreglo(arreglo,tempReturn,expresiones,generador)
        
        if arreglo.tipoStruct == Type.BOOL:
            ret = Return(tempReturn,arreglo.tipoStruct,True)
            ret.trueLb = generador.newLabel()
            ret.falseLb = generador.newLabel()
            generador.addIf(tempReturn,'1','==',ret.trueLb)
            generador.addGoto(ret.falseLb) 
            return ret 
        elif arreglo.tipoStruct==Type.STRING:
            generador.addExpresion(indiceAcceso,'','','H')
            generador.addExpresion('H','2','+','H')
            return Return(returnAux,arreglo.tipoStruct,True)

        return Return(tempReturn,arreglo.tipoStruct,True)

    def buscarEnArreglo(self,arreglo:Simbolo,posOnH,expresiones,generador:Generator):
        expreActual:Return = expresiones.pop()
        if expreActual.tipo!=Type.INT:
                print("Expresion de acceso a arreglo invalida")
                return Return(0,arreglo.tipoStruct)
        
        posicionArreglo = generador.addTemporal()
        generador.addExpresion(posOnH,'','',posicionArreglo)

        tempTamano = generador.addTemporal()
        labelContinue = generador.newLabel()
        labelError = generador.newLabel()
        salida = generador.newLabel()

        generador.getHeap(tempTamano,posicionArreglo)
        generador.addIf(expreActual.valor,tempTamano,'>',labelError)
        generador.addGoto(labelContinue)

        generador.putLabel(labelContinue)
        indiceAcceso = generador.addTemporal()
        generador.addExpresion(expreActual.valor,posicionArreglo,'+',indiceAcceso)
        tempReturn = generador.addTemporal()
        generador.getHeap(tempReturn,indiceAcceso)
        generador.addGoto(salida)

        generador.putLabel(labelError)
        generador.funcErrorArrego()
        generador.callFun("boundsError")
        generador.addExpresion('0','','',tempReturn)
        generador.addGoto(salida)
        generador.putLabel(salida)

        if len(expresiones) !=0:
            return self.buscarEnArreglo(arreglo,tempReturn,expresiones,generador)

        if arreglo.tipoStruct == Type.BOOL:
            ret = Return(tempReturn,arreglo.tipoStruct,True)
            ret.trueLb = generador.newLabel()
            ret.falseLb = generador.newLabel()
            generador.addIf(tempReturn,'1','==',ret.trueLb)
            generador.addGoto(ret.falseLb) 
            return ret 
        

        return Return(tempReturn,arreglo.tipoStruct,True)