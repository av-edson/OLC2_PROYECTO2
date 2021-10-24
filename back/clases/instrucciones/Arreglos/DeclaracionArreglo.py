from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator

class DeclaracionArreglo(Expresion):
    def __init__(self,expresiones, line, column,tipoAux=None):
        Expresion.__init__(self,line, column)
        self.expresiones = expresiones
        self.size = len(expresiones)
        self.tipoAux = tipoAux

    def compilar(self, enviroment):
        try:
            genAux = Generator()
            generator = genAux.getInstance()

            listaValores = []
            for expre in self.expresiones:
                ret:Return = expre.compilar(enviroment)
                if ret is None:
                    print("expresion dentro de arreglo arrojo Nono")
                    generator.addExpresion('H','1','-','H')
                    return Return()
                if ret.tipo == Type.UNDEFINED or ret.tipo==Type.RETURNST or ret.tipo==Type.BREACKST or ret.tipo==Type.CONTINUEST:
                    print("Una de las expresiones del arreglo tiene error o no se admite")
                    generator.addExpresion('H','1','-','H')
                    return Return()
                listaValores.append(ret)


            tempRetorno = generator.addTemporal()
            generator.addExpresion('H','','',tempRetorno)
            generator.setHeap('H',self.size)
            generator.nextHeap()

            for valor in listaValores:
                generator.setHeap('H',valor.valor)
                generator.nextHeap()

            return  Return(tempRetorno,Type.ARRAY,True,self.tipoAux)

        except:
            print("Ocurrio un error en la declaracion de arreglo")
