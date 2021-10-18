from clases.enviroment.Generator import Generator
from clases.abstract.Return import *
from clases.abstract.Instruccion import Instruccion
from enum import Enum

class TipoImpresion(Enum):
    PRINT=0
    PRINTLN=1

class Imprimir(Instruccion):
    def __init__(self,listaExpresiones,tipo, line, column):
        Instruccion.__init__(self,line, column)
        self.tipo=tipo
        self.listaExpre = listaExpresiones
    def compilar(self, enviroment):
        try:
            lista = []
            for exp in self.listaExpre:
                res:Return = exp.compilar(enviroment)
                if res.tipo == Type.UNDEFINED:
                    print("una de las expresiones en el print tiene error")
                    return
                # ver los demas tipos de datos
                lista.append(res)   
            if self.tipo==TipoImpresion.PRINT:
                self.ImprimirSimple(lista,enviroment)
            else: self.ImprimirML(lista,enviroment)
        except:
            print("error inesperado en el print")
        
    def ImprimirSimple(self,lista,enviroment):
        genAux = Generator()
        generador = genAux.getInstance()
        generador.addComent("Inicio Impresion")
        for expre in lista:
            if expre.tipo == Type.INT:
                generador.addPrint("d",expre.valor)
            elif expre.tipo == Type.FLOAT:
                generador.addPrint("f",expre.valor)
            elif expre.tipo == Type.BOOL:
                tempLbl = generador.newLabel()
            
                generador.putLabel(expre.trueLb)
                generador.printTrue()

                generador.addGoto(tempLbl)

                generador.putLabel(expre.falseLb)
                generador.printFalse()

                generador.putLabel(tempLbl)
            elif expre.tipo == Type.STRING:
                generador.funPrintString()
                temporalParametro = generador.addTemporal()
                generador.addExpresion('P',enviroment.size,'+',temporalParametro)
                generador.addExpresion(temporalParametro,'1','+',temporalParametro)

                generador.newEnv(enviroment.size)
                generador.callFun('printString')
                temp = generador.addTemporal()
                generador.getStack(temp,'P')
                generador.retEnv(enviroment.size)
                generador.addExpresion(expre.valor,'','','H')
            elif expre.tipo==Type.CHAR:
                generador.addPrint('c',expre.valor)

        generador.addPrint("c",10)
        generador.addComent("Fin Impresion")
    
    def ImprimirML(self, lista,enviroment):
        genAux = Generator()
        generador = genAux.getInstance()
        generador.addComent("Inicio Impresion")
        for expre in lista:
            if expre.tipo == Type.INT:
                generador.addPrint("d",expre.valor)
            elif expre.tipo == Type.FLOAT:
                generador.addPrint("f",expre.valor)
            elif expre.tipo==Type.STRING:
                generador.funPrintString()
                temporalParametro = generador.addTemporal()
                generador.addExpresion('P',enviroment.size,'+',temporalParametro)
                generador.addExpresion(temporalParametro,'1','+',temporalParametro)

                generador.newEnv(enviroment.size)
                generador.callFun('printString')
                temp = generador.addTemporal()
                generador.getStack(temp,'P')
                generador.retEnv(enviroment.size)
                generador.addExpresion(expre.valor,'','','H')
            generador.addPrint("c",10)
            generador.addComent("Fin Impresion")
