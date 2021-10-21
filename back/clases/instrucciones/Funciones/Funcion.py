from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import Type
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from clases.instrucciones.Funciones.Parametro import Parametro

class Funcion(Instruccion):
    def __init__(self,identificador,instrucciones,parametros,tipo, line, column):
        Instruccion.__init__(self,line, column)
        self.ide = identificador
        self.instrucciones = instrucciones
        self.parametros = parametros
        self.tipo = tipo

    def compilar(self, enviroment:Enviroment):
        try:
            enviroment.saveFuncion(self.ide,self)
            aux = Generator()
            generador = aux.getInstance()
            entornoInterno = Enviroment(enviroment,"Funcion: "+str(self.ide))
            labelReturn = generador.newLabel()
            entornoInterno.lbReturn = labelReturn
            entornoInterno.size = 1

            for parametro in self.parametros:
                parametro:Parametro = parametro
                entornoInterno.sabeVar(parametro.id,parametro.tipo,(parametro.tipo==Type.STRING or parametro.tipo==Type.STRUCT))

            generador.addInicioFuncion(self.ide)
            ret = self.instrucciones.compilar(entornoInterno)

            if self.tipo is None:
                generador.addGoto(labelReturn)

            generador.putLabel(labelReturn)
            generador.addEndFuncion()
            if ret != None:
                return ret

        except:
            print("error en la creacion de la funcion "+str(self.ide))

        