from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
from enum import Enum, auto

class TipoRelacional(Enum):
    MAYOR = 1
    MENOR = 2
    MAYOR_IGUAL = 3
    MENOR_IGUAL = 4
    IGUAL_IGUAL = 5
    DIFERENTE = 6

class OperacionRelacional(Expresion):
    def __init__(self,izquierdo,derecho,tipo, line, column):
        Expresion.__init__(self,line, column)
        self.izq = izquierdo
        self.der = derecho
        self.tipo = tipo

    def compilar(self, enviroment):
        try:
            aux = Generator()
            generator = aux.getInstance()
            generator.addComent("Inicio DE EXPRESION RELACIONAL")

            dere = None    
            izqi:Return = self.izq.compilar(enviroment)
            res = Return(0,Type.BOOL,False)

            if izqi.tipo != Type.BOOL:
                dere = self.der.compilar(enviroment)
                # COMPARACION NUMEROS
                if (izqi.tipo==Type.INT or izqi.tipo==Type.FLOAT) or (dere.tipo==Type.INT or dere.tipo==Type.FLOAT):
                    self.verLabels()
                    generator.addIf(izqi.valor, dere.valor, self.getOperation(), self.trueLb)
                    generator.addGoto(self.falseLb)
                elif izqi.tipo==Type.STRING and dere.tipo==Type.STRING:
                    print("falta hacer esto")
            else:
                if not(self.tipo==TipoRelacional.IGUAL_IGUAL or self.tipo==TipoRelacional.DIFERENTE):
                    print("no se admite booleanos en operaciones relacionales")
                    return Return()
                gotoRigth = generator.newLabel()
                tempIzq = generator.addTemporal()

                generator.putLabel(izqi.trueLb)
                generator.addExpresion('1','','',tempIzq)
                generator.addGoto(gotoRigth)

                generator.putLabel(izqi.falseLb)
                generator.addExpresion('0', '', '', tempIzq)

                generator.putLabel(gotoRigth)

                right = self.der.compilar(enviroment)
                if right.tipo != Type.BOOL:
                    print("Tipo de dato no booleano en comparacion")
                    return
                gotoEnd = generator.newLabel()
                rightTemp = generator.addTemporal()

                generator.putLabel(right.trueLb)

                generator.addExpresion( '1', '', '',rightTemp)
                generator.addGoto(gotoEnd)

                generator.putLabel(right.falseLb)
                generator.addExpresion('0', '', '',rightTemp)

                generator.putLabel(gotoEnd)

                self.verLabels()
                generator.addIf(tempIzq, rightTemp, self.getOperation(), self.trueLb)
                generator.addGoto(self.falseLb)

            generator.addComent("FIN DE EXPRESION RELACIONAL")
            res.trueLb = self.trueLb
            res.falseLb = self.falseLb

            return res  
        except:
            print("error inesperado en operacion relacional")

    def verLabels(self):
        aux = Generator()
        generator = aux.getInstance()
        if self.trueLb == '':
            self.trueLb = generator.newLabel()
        if self.falseLb == '':
            self.falseLb = generator.newLabel()
    
    def getOperation(self):
        if self.tipo==TipoRelacional.MAYOR:
            return ">"
        elif self.tipo==TipoRelacional.MENOR:
            return "<"
        elif self.tipo==TipoRelacional.MAYOR_IGUAL:
            return ">="
        elif self.tipo==TipoRelacional.MENOR_IGUAL:
            return "<="
        elif self.tipo==TipoRelacional.DIFERENTE:
            return "!="
        elif self.tipo==TipoRelacional.IGUAL_IGUAL:
            return "=="
