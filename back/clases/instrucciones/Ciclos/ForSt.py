from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import *
from clases.instrucciones.BloqueInstrucciones import BloqueInstrucciones
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from clases.instrucciones.Declaracion import Declaracion
from clases.expresiones.Variable import LLamadaVariable
from clases.expresiones.Literal import ExpresionLiteral

class CicloFor(Instruccion):
    def __init__(self,varControl,expre1,bloque, line, column,expre2=None):
        Instruccion.__init__(self,line, column)
        self.variable=varControl
        self.expr1 = expre1
        self.expr2 = expre2
        self.bloque:BloqueInstrucciones = bloque
    
    def compilar(self, enviroment):
        try:
            aux = Generator()
            generador = aux.getInstance()

            generador.addComent("Inicio ciclo for")
            entornoInterno:Enviroment = Enviroment(enviroment,"Ciclo For"+str(self.line))
            if self.expr2 != None:
                # asignacion de variable index
                inicio:Return = self.expr1.compilar(entornoInterno)
                fin:Return = self.expr2.compilar(entornoInterno)
                if inicio.tipo!=Type.INT or fin.tipo!=Type.INT:
                    print("expresion del for no es de tipo entero")
                    generador.addComent("Fin ciclo for")
                    return
                declaracion = Declaracion(self.variable,ExpresionLiteral(inicio.tipo,inicio.valor,self.line,self.column),self.line,self.column)
                declaracion.compilar(entornoInterno)

                temporalFin = generador.addTemporal()
                generador.addExpresion(fin.valor,'','',temporalFin)
                labelCiclo = generador.newLabel()
                labelSalida = generador.newLabel()
                generador.addGoto(labelCiclo)

                entornoInterno.lbBreack = labelSalida

                generador.putLabel(labelCiclo)
                llamada = LLamadaVariable(self.variable,self.line,self.column)
                reg:Return = llamada.compilar(entornoInterno)

                generador.addIf(reg.valor,temporalFin,'>',labelSalida)

                self.bloque.compilar(entornoInterno)

                declaracion = Declaracion(self.variable,ExpresionLiteral(inicio.tipo,reg.valor,self.line,self.column),self.line,self.column)
                generador.addExpresion(reg.valor,'1','+',reg.valor)
                declaracion.compilar(entornoInterno)
                generador.addGoto(labelCiclo)

                generador.putLabel(labelSalida)
            #------------------------ ciclo con arrerglo o string -----------------------------
            else:
                ret:Return = self.expr1.compilar(entornoInterno)
                if not (ret.tipo==Type.STRING or ret.tipo==Type.ARRAY):
                    print("expresion no valida para el for")
                    return
                if ret.tipo==Type.STRING:
                    print("falta implementarlo")
                    return
                    #index = generador.addTemporal()
                    #generador.addExpresion('H','2','-',index)
                    #generador.getHeap(index,index)
                    #labelSalida = generador.newLabel()
                    #generador.addComent("declaracion string")
                    #palabra = generador.addTemporal()
                    #generador.getHeap(palabra,index)
                    #
                    #declaracion = Declaracion(self.variable,)
#
                    #labelCiclo = generador.newLabel()
                    #generador.addGoto(labelCiclo)
                    #entornoInterno.lbBreack = labelSalida
#
                    #generador.putLabel(labelCiclo)
                    #llamada = LLamadaVariable(self.variable,self.line,self.column)
                    #reg:Return = llamada.compilar(entornoInterno)

                    
        except:
            print("error inesperado en el ciclo for")
            return
