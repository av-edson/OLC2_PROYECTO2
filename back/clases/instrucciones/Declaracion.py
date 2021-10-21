from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from clases.abstract.Instruccion import *
from clases.abstract.Return import *

class Declaracion(Instruccion):
    def __init__(self,id,valor, line, column,esGlobal=False,tipo=None):
        Instruccion.__init__(self,line, column)
        self.id = id
        self.valor = valor
        self.tipo=tipo
        self.esGlobal=None
        '''
            global = None -> variable norma
            global = True -> variable global
            global = False -> variable local
        '''
    
    def compilar(self, enviroment:Enviroment):
        aux = Generator()
        generador = aux.getInstance()

        generador.addComent("Inicio Declaracion")
        valor = self.valor.compilar(enviroment)

        # codigo ingresado por mi xd
        if valor.tipo==Type.UNDEFINED:
            return
        if self.tipo!=None:
            if self.tipo!=valor.tipo:
                print("no coincide tipo de valor con declaracion")
                generador.addComent("Fin Declaracion")
                return
        nueva = enviroment.getVariable(self.id,self.esGlobal)
        if nueva == None:
            aux = (valor.tipo==Type.STRING or valor.tipo==Type.STRUCT)
            glo = aux
            if self.esGlobal is not None:
                glo = glo or self.esGlobal
            if not aux:
                nueva = enviroment.sabeVar(self.id,valor.tipo,aux,None,glo)
            elif valor.tipo == Type.STRING:
                nueva = enviroment.sabeVar(self.id,self.tipo,True,None,glo)
            else:
                print("declaracion structs y listas falta")
        
        nueva.tipo = valor.tipo

        #posicion de la variable
        temporalPosicion = nueva.posicion
        if (not nueva.globalVar):
            temporalPosicion = generador.addTemporal()
            generador.addExpresion('P',nueva.posicion,'+',temporalPosicion)

        if (valor.tipo==Type.BOOL):
            tempLb = generador.newLabel()

            generador.putLabel(valor.trueLb)
            generador.setStack(temporalPosicion,'1')

            generador.addGoto(tempLb)

            generador.putLabel(valor.falseLb)
            generador.setStack(temporalPosicion,'0')
            
            generador.putLabel(tempLb)
        elif valor.tipo==Type.STRING:
            generador.addComent("declaracion string")
            generador.setStack(temporalPosicion,valor.valor)
        else:
            generador.setStack(temporalPosicion,valor.valor)

        generador.addComent("Fin Declaracion")
