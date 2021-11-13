from clases.abstract.Expresion import Expresion
from enum import Enum

from clases.abstract.Return import Return, Type
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class TipoNativa(Enum):
    PARSE=0
    TRUNC=1
    STRING=2
    LENGTH=3

class Nativa(Expresion):
    def __init__(self,parametros,tipo, line, column):
        Expresion.__init__(self,line, column)
        self.parametros = parametros
        self.tipo:TipoNativa = tipo

    def compilar(self, enviroment):
        if self.tipo==TipoNativa.LENGTH: return self.getSize(self.parametros,enviroment)
        elif self.tipo==TipoNativa.TRUNC: return self.funTrunc(self.parametros,enviroment)
    
    def getSize(self,id,enviroment:Enviroment):
        variable = enviroment.getVariable(id)
        aux = Generator()
        generador = aux.getInstance()
        if variable is None:
            print("Identificador dentro de lenght no existe")
            return Return(0,Type.INT)
        if variable.tipo!=Type.ARRAY:
            print("No es un Arreglo")
            return Return(0,Type.INT)
        
        posicionArreglo = generador.addTemporal()
        posicion = variable.posicion

        if not(variable.globalVar):
            posicion = generador.addTemporal()
            generador.addExpresion('P',variable.posicion,'+',posicion)
        generador.getStack(posicionArreglo,posicion)

        tamano = generador.addTemporal()
        generador.getHeap(tamano,posicionArreglo)

        return Return(tamano,Type.INT,True)

    def funTrunc(self,id,envitoment:Enviroment):
        aux = Generator()
        generador = aux.getInstance()

        expre:Return = id.compilar(envitoment)
        if not ( expre.tipo==Type.INT or expre.tipo==Type.FLOAT): 
            print("expresion no admitida para modulo")
            return Return()
        aux = generador.addTemporal()
        regreso = generador.addTemporal()
        generador.addExpresion(expre.valor,'','',aux)
        generador.activarModulo(aux,'1',aux)
        generador.addExpresion(expre.valor,aux,'-',regreso)
        expre.tipo=Type.INT
        expre.valor=regreso
        return expre


