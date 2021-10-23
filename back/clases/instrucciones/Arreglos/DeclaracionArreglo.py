from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator

class DeclaracionArreglo(Expresion):
    def __init__(self,expresiones, line, column,tipoAux):
        Expresion.__init__(self,line, column)
        self.expresiones = expresiones
        self.size = len(expresiones)
        self.tipoAux = tipoAux

    def compilar(self, enviroment):
        try:
            listaValores = []
            genAux = Generator()
            generator = genAux.getInstance()
            
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

            self.size = len(listaValores)
            generator.setHeap('H',self.size)
            generator.nextHeap()

            for valor in listaValores:
                if valor.tipo == Type.INT or valor.tipo==Type.FLOAT:
                    valor:Return = valor
                    generator.setHeap('H',valor.valor)
                    generator.nextHeap()
                elif valor.tipo == Type.ARRAY:
                    generator.setHeap('H',valor.valor)
                    generator.nextHeap()
            #generator.setHeap('H','-1')
            #generator.nextHeap()

            return  Return(tempRetorno,Type.ARRAY,True,self.tipoAux)

        except:
            print("Ocurrio un error en la declaracion de arreglo")
