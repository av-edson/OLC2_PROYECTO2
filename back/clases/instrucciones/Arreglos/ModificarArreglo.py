from clases.abstract.Instruccion import *
from clases.abstract.Return import Return, Type
from clases.enviroment.Generator import Generator
from clases.enviroment.Simbol import Simbolo

class ModificarArreglo(Instruccion):
    def __init__(self,id,listaAcceso,expresion, line, column):
        Instruccion.__init__(self,line, column)
        self.id= id
        self.listaAcceso = listaAcceso
        self.expresion = expresion
    
    def compilar(self, enviroment):
        try:
            nuevo:Return = self.expresion.compilar(enviroment)
            variable:Simbolo = enviroment.getVariable(self.id)
            aux = Generator()
            generador = aux.getInstance()
            generador.addComent("Modificacion Arreglo")
            if variable is None:
                print("Arreglo a modificar no existe")
                return
            if variable.tipoStruct != nuevo.tipo:
                if variable.primitivo!=nuevo.tipo:
                    print("Tipo de dato no coincide con el del arreglo")
                return

            posicionArreglo = generador.addTemporal()
            posicion = variable.posicion

            returnAux = generador.addTemporal()
            generador.addExpresion('H','','',returnAux)

            if not(variable.globalVar):
                posicion = generador.addTemporal()
                generador.addExpresion('P',variable.posicion,'+',posicion)
            generador.getStack(posicionArreglo,posicion)

            listado = self.listaAcceso.copy()
            listado.reverse()
            aux = []
            for expre in listado:
                ret = expre.compilar(enviroment)
                aux.append(ret)
            
            self.modificarArreglo(variable,posicionArreglo,aux,generador,nuevo)

            if variable.tipoStruct==Type.STRING:
                generador.addExpresion(returnAux,'','','H')
        except:
            print("Error inesperado en la modificacion de arreglo")
            return

    def modificarArreglo(self,arreglo:Simbolo,posOnH,expresiones,generador:Generator,nuevo:Return):
        expreActual = expresiones.pop()
        if expreActual.tipo!=Type.INT:
                print("Expresion de acceso a arreglo invalida")
                return Return(0,arreglo.tipoStruct)

        tempTamano = generador.addTemporal()
        labelContinue = generador.newLabel()
        labelError = generador.newLabel()
        salida = generador.newLabel()

        generador.getHeap(tempTamano,posOnH)
        generador.addIf(expreActual.valor,tempTamano,'>',labelError)
        generador.addGoto(labelContinue)

        generador.putLabel(labelContinue)
        indiceAcceso = generador.addTemporal()
        generador.addExpresion(expreActual.valor,posOnH,'+',indiceAcceso)
        if len(expresiones)==0:
            generador.setHeap(indiceAcceso,nuevo.valor)
        generador.addGoto(salida)

        generador.putLabel(labelError)
        generador.funcErrorArrego()
        generador.callFun("boundsError")
        generador.addGoto(salida)
        
        generador.putLabel(salida)

        if len(expresiones) !=0:
            tempReturn = generador.addTemporal()
            generador.getHeap(tempReturn,indiceAcceso)
            return self.modificarArreglo(arreglo,tempReturn,expresiones,generador,nuevo)

