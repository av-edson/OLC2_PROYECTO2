from clases.abstract.Return import *
from clases.abstract.Expresion import *
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

class LLamadaVariable(Expresion):
    def __init__(self,id, line, column):
        Expresion.__init__(self,line, column)
        self.id = id

    def compilar(self, enviroment:Enviroment):
        try:
            aux = Generator()
            generador = aux.getInstance()
            generador.addComent("LLamada Variable")

            variable = enviroment.getVariable(self.id)
            if variable==None:
                print("variable no existe "+self.id)
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
            elif variable.tipo==Type.STRING:
                #index = generador.addTemporal()
                ret = generador.addTemporal()
                generador.addExpresion('H','','',ret)   # a1 = H
                generador.addExpresion(temp,'1','-',temp)   #t2 = t2 - 1
                labelCiclo = generador.newLabel()
                labelSalida = generador.newLabel()
                generador.addGoto(labelCiclo)               #goto L66
                generador.putLabel(labelCiclo)              #L6:
                
                generador.addExpresion(temp,'1','+',temp)
                comparador = generador.addTemporal()
                generador.getHeap(comparador,temp)
                generador.addIf(comparador,'-1','==',labelSalida)
                generador.setHeap('H',comparador)
                generador.nextHeap()
                generador.addGoto(labelCiclo)

                generador.putLabel(labelSalida)
                generador.setHeap('H','-1')
                generador.nextHeap()
                generador.setHeap('H',ret)
                generador.nextHeap()
                generador.setHeap('H','-1')
                generador.nextHeap()

                generador.addComent("Fin llamada Variable")
                return Return(ret,Type.STRING,True)

            return Return()
        except:
            print('----Error al ejecutar funcion nativa')
            return Return()
        


