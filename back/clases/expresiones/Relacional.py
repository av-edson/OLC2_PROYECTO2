from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
from clases.enviroment.auxGenerador import auxGenerador
from enum import Enum

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
                dere:Return = self.der.compilar(enviroment)
                # COMPARACION NUMEROS
                if (izqi.tipo==Type.INT or izqi.tipo==Type.FLOAT) or (dere.tipo==Type.INT or dere.tipo==Type.FLOAT):
                    self.verLabels()
                    generator.addIf(izqi.valor, dere.valor, self.getOperation(), self.trueLb)
                    generator.addGoto(self.falseLb)
                # COMPARACION CADENAS
                elif izqi.tipo==Type.STRING and dere.tipo==Type.STRING:
                    if not(self.tipo==TipoRelacional.IGUAL_IGUAL or self.tipo==TipoRelacional.DIFERENTE):
                        return self.comparacionString(izqi,dere)
                    generator.setHeap('H',izqi.valor)
                    generator.nextHeap()
                    generator.setHeap('H',dere.valor)
                    generator.nextHeap()
                    generator.setHeap('H','-1')
                    generator.nextHeap()
                    # llamamos a crear la funcion nativa
                    aux = auxGenerador()
                    if self.getOperation() == "==":
                        aux.CompararString('!=')
                    elif self.getOperation() == "!=":
                        aux.CompararString('==')
                    # llamamos a la funcion
                    generator.callFun("igualarString")
                    valorRetorno = generator.addTemporal()
                    generator.addExpresion('H','2','-',valorRetorno)
                    generator.getHeap(valorRetorno,valorRetorno)
                    generator.addExpresion(izqi.valor,'','','H')

                    self.verLabels()
                    generator.addIf(valorRetorno,'1',self.getOperation(),self.trueLb)
                    generator.addGoto(self.falseLb)
                else:
                    print("tipo de dato no admitido en operacion relacional")
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

    def comparacionString(self,izq,der):
        aux = Generator()
        generador = aux.getInstance()
        generador.addComent("Inicio Relacional Cadenas")
        index1 = generador.addTemporal()
        index2 = generador.addTemporal()
        generador.addExpresion(izq.valor,'','',index1)
        generador.addExpresion(der.valor,'','',index2)
        #index1 = izq.valor
        #index2 = der.valor
        palabra1 = generador.addTemporal()
        palabra2 = generador.addTemporal()
        primerCiclo = generador.newLabel()
        segundoCiclo = generador.newLabel()
        salida = generador.newLabel()

        generador.putLabel(primerCiclo)
        generador.getHeap(palabra1,index1)
        generador.addIf(palabra1,'-1','==',segundoCiclo)
        generador.addExpresion(index1,'1','+',index1)
        generador.addGoto(primerCiclo)

        generador.putLabel(segundoCiclo)
        generador.getHeap(palabra2,index2)
        generador.addIf(palabra2,'-1','==',salida)
        generador.addExpresion(index2,'1','+',index2)
        generador.addGoto(segundoCiclo)

        generador.putLabel(salida)
        generador.addExpresion(izq.valor,'','','H')
        generador.addExpresion(index1,izq.valor,'-',index1)
        generador.addExpresion(index2,der.valor,'-',index2)
        ## los label de verdadero y falso
        self.verLabels()
        generador.addIf(index1,index2,self.getOperation(),self.trueLb)
        generador.addGoto(self.falseLb)
        res = Return(0,Type.BOOL,False)

        generador.addComent("Fin Relacional Cadenas")
        res.trueLb = self.trueLb
        res.falseLb = self.falseLb
        
        return res 